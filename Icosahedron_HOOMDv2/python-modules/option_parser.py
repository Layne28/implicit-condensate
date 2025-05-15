# This module contains simple functions to parse config files.
from __future__ import print_function
import sys

# An "enum" for some stuff.
UNREC_POL_WARN = 0
UNREC_POL_ABORT = 1

def strip_char( string, char ):
    """ Returns string up to but without char. """
    return string.split(char)[0].rstrip()




class file_parser:
    """ Reads a file and stores options. """
    def __init__( self ):
        """ Init the options dictionary. """
        self.options = {}
        self.default_type = str
        self.unrec_pol = UNREC_POL_WARN

    def add_option( self, name, opt_type, default_val = None ):
        """ Adds an option with a type and a default value """
        self.options[ name ] = [ default_val, opt_type ]

    def print_options( self, fp ):
        """ Prints all options to given file """
        for opt in self.options:
            print( opt, file = fp )

    def parse_option_pair( self, key, rest ):
        """ Parses a given key/rest pair. """
        if not key in self.options:
            if self.unrec_pol == UNREC_POL_ABORT:
                print( "Unrecognized key", key, "encountered! Aborting!",
                       file = sys.stderr )
                return None
            elif self.unrec_pol == UNREC_POL_WARN:
                print( "Warning! Unrecognized key", key, "encountered!",
                       file = sys.stderr )
        else:
            val_default = self.options[ key ][0]
            val_type    = self.options[ key ][1]
            rest = rest.strip()
                    
            if val_type == bool:
                # Python's parser is stupid.
                if rest == '0':
                    return ( False, rest )
                else:
                    return ( True, rest )
            elif val_type == 'float_list' or val_type == 'int_list':
                print( "Got a list for ", key ,":",
                       val_type, file = sys.stderr )
                # Read the list in properly.
                contents = rest.split()
                dtype = float
                if val_type == 'int_list':
                    dtype = int
                elif val_type == 'float_list':
                    dtype = float
                else:
                    print( "Unknown list type ", val_type, "!",
                           file = sys.stderr )
                    return None
                values = []
                for c in contents:
                    if c == '[' or c == ']': continue
                    
                    values.append( dtype(c) )
                return ( values, rest )
            else:
                return ( val_type( rest ), rest )

    def replace_unset_with_defaults( self, opts ):
        """ Replaces unset options with the defaults. """
        for opt in self.options:
            if not opt in opts:
                opts[opt] = ( self.options[opt][0],
                              str( self.options[opt][0] ) )
        return opts

    def parse_unrec_pol( self, unrecognized_policy ):
        """ Parses the unrecognized policy. """
        if unrecognized_policy == None:
            return UNREC_POL_WARN
        elif unrecognized_policy == "warn":
            return UNREC_POL_WARN
        elif unrecognized_policy == "abort":
            return UNREC_POL_ABORT
        else:
            return None

    
    def read_file( self, fname, unrecognized_policy = None ):
        """ Reads in given file and parses all options. """

        self.unrec_pol = self.parse_unrec_pol( unrecognized_policy )
        if self.unrec_pol is None:
            print( "Unrecognized policy", unrecognized_policy,
                   file = sys.stderr )
            return None

        opts = {}
        opts = self.set_from_file( fname, opts, unrecognized_policy )
        
        opts = self.replace_unset_with_defaults( opts )
        return opts

    def read_cmd_line( self, argv, unrecognized_policy = None ):
        """ Reads options from the command line. """
        self.unrec_pol = self.parse_unrec_pol( unrecognized_policy )
        if self.unrec_pol is None:
            print( "Unrecognized policy", unrecognized_policy,
                   file = sys.stderr )
            return None
        opts = {}
        opts = self.set_from_cmdline( argv, opts, unrecognized_policy )
        
        opts = self.replace_unset_with_defaults( opts )
        return opts

    def set_from_cmdline( self, argv, opts, unrecognized_policy = None ):
        """ Sets options from command line. """
        nopts = 0
        argc = len(argv)
        i = 0
        
        while i < argc:
            key = argv[i]
            if len(key) < 2 or not key[0:2] == "--":
                raise RuntimeError( "Cannot parse arg", key, "!" )
            key = key[2:]
            if i+1 == argc:
                raise RuntimeError( "Key", key, "requires an argument!" )
            rest = argv[i+1]
            if rest == '[':
                # You got a list. Read stuff until you find the closing brace.
                j = 2
                while argv[i+j] != ']':
                    rest += ' '
                    rest += argv[i+j]
                    j += 1
                rest += ' ]'
                i += j + 1
            else:
                i += 2
            
            value_rest_pair = self.parse_option_pair( key, rest )
            opts[ key ] = value_rest_pair
            nopts += 1
        print("Read {} options from command line.".format(nopts),
              file = sys.stderr )
        return opts

    def set_from_file( self, fname, opts, unrecognized_policy = None ):
        """ Sets options from file. """
        with open( fname, "r" ) as fp:
            nopts = 0
            while True:
                line = fp.readline()
                if line == "":
                    break

                l = strip_char( line.rstrip(), '#' )
                if l == "": continue
                
                words = l.split('=')
                key = words[0].rstrip()
                rest = words[1].rstrip()

                value_rest_pair = self.parse_option_pair( key, rest )
                opts[ key ] = value_rest_pair
                nopts += 1

        print("Read {} options from file {}.".format(nopts, fname),
              file = sys.stderr )
        return opts
        
    def write( self, fname, opts, header = None ):
        """ Writes options to given file name. """
        with open( fname, "w" ) as fp:
            if header is None:
                print( ("# This is a config file that contains the options as "
                        "parsed by option_parser"), file = fp )
            else:
                if not header.startswith( '#' ):
                    header = '#' + header
                print( header, file = fp )
            for key in opts:
                opt_val = opts[key]
                if opt_val is None or opt_val[0] == '':
                    print( "Skipping empty option", key, file = sys.stderr )
                    continue

                # Because we kept the string representation, this is easy:
                print( key, "=", opt_val[1], file = fp )
                


if __name__ == "__main__":
    """ Do nothing. """

     
