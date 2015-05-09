import click
import sys

import cmd
import thrift_client
    

class Cli(cmd.Cmd):
    def __init__(self, conn):
        cmd.Cmd.__init__(self)
        self.__conn = conn
        self.__client = conn.client

    def do_exit(self, line):
        return True

    def default(self, line):
        try:
            res = self.__client.ExecuteStatement(thrift_client.TExecuteStatementReq(line))
        except thrift_client.TOperationalError as e:
            print "Error: %s" % e.message
            return

        
        for row in res.rows:

            row_values = []
            for val in row.colVals:
                if val.boolVal is not None:
                    str_val = str(val.boolVal.value)
                elif val.i32Val is not None:
                    str_val = str(val.i32Val.value)
                elif val.doubleVal is not None:
                    str_val = str(val.doubleVal.value)
                elif val.stringVal is not None:
                    str_val = str(val.stringVal.value)
                else:
                    str_val = 'NULL'

                row_values.append(str_val)

            print '|'.join(row_values)

    
@click.command()
@click.option('--hostname', help='Hostname', default='localhost')
@click.option('--port', help='Port', default=8080)
def client(hostname, port):

    conn = thrift_client.connect(hostname, port)
    client = conn.client

    Cli(conn).cmdloop()

    conn.close()
    
    
        
if __name__ == '__main__':
    client()




