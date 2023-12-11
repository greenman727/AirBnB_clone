#!/usr/bin/python3
"""Defines the HBNB console commands."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


def parse(arg):
    """Defines parse"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines HBNBCommand"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Empty module."""
        pass

    def default(self, arg):
        """Default value for cmd module when there is error."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arglen = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arglen[1])
            if match is not None:
                command = [arglen[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arglen[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quits the program."""
        return True

    def do_EOF(self, arg):
        """Exit commmand."""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, save it to JSON."""
        arglen = parse(arg)
        if len(arglen) == 0:
            print("** class name missing **")
        elif arglen[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arglen[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        arglen = parse(arg)
        objdict = storage.all()
        if len(arglen) == 0:
            print("** class name missing **")
        elif arglen[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arglen) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglen[0], arglen[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arglen[0], arglen[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        arglen = parse(arg)
        objdict = storage.all()
        if len(arglen) == 0:
            print("** class name missing **")
        elif arglen[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arglen) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglen[0], arglen[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arglen[0], arglen[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        arglen = parse(arg)
        if len(arglen) > 0 and arglen[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arglen) > 0 and arglen[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arglen) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Counts number ofarguments."""
        arglen = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arglen[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """ Updates an instance based on the class name and id."""
        arglen = parse(arg)
        objdict = storage.all()

        if len(arglen) == 0:
            print("** class name missing **")
            return False
        if arglen[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arglen) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arglen[0], arglen[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arglen) == 2:
            print("** attribute name missing **")
            return False
        if len(arglen) == 3:
            try:
                type(eval(arglen[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arglen) == 4:
            obj = objdict["{}.{}".format(arglen[0], arglen[1])]
            if arglen[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arglen[2]])
                obj.__dict__[arglen[2]] = valtype(arglen[3])
            else:
                obj.__dict__[arglen[2]] = arglen[3]
        elif type(eval(arglen[2])) == dict:
            obj = objdict["{}.{}".format(arglen[0], arglen[1])]
            for k, v in eval(arglen[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()   
