import click

import logging
logging.basicConfig()

@click.command()
@click.option('--path', prompt='Sqlite database', help='Sqlite full path db.')
def server(path):
    import thrift_server
    thrift_server.serve(8080, path)
    
        
if __name__ == '__main__':
    server()



