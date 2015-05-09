import sys, glob

from gen_py.sqlite_server import ThriftVtor
from gen_py.sqlite_server.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from sqlite3 import connect, OperationalError


def create_response_row(raw_row):
    values = []

    for value in raw_row:
      value_type = type(value)
      res_value = TColumnValue()
            
      if value_type == bool:
        res_value.boolVal = TBoolValue(value)
      elif value_type == int:
        res_value.i32Val = TI32Value(value)
      elif value_type == float:
        res_value.doubleVal = TDoubleValue(value)
      elif (value_type == str) or (value_type == unicode):
        res_value.stringVal = TStringValue(value)
      values.append(res_value)

    return TRow(values)

class ThriftVtorHandler:
  def __init__(self, path):

    try:
        self.__conn = connect(path, check_same_thread=False)
    except OperationalError as e:
        print 'Cannot open database "%s"' % path
        raise e

  

  def ExecuteStatement(self, req):
    cursor = self.__conn.cursor()
    
    try:
      cursor.execute(req.statement)
    except OperationalError as e:
      raise TOperationalError(repr(e))


    rows = [create_response_row(row) for row in cursor]    
    
    cursor.close()

    return TExecuteStatementResp(rows)

    

  # def ping(self):
  #   print 'ping()'

  # def add(self, n1, n2):
  #   print 'add(%d,%d)' % (n1, n2)
  #   return n1+n2

  # def calculate(self, logid, work):
  #   print 'calculate(%d, %r)' % (logid, work)

  #   if work.op == Operation.ADD:
  #     val = work.num1 + work.num2
  #   elif work.op == Operation.SUBTRACT:
  #     val = work.num1 - work.num2
  #   elif work.op == Operation.MULTIPLY:
  #     val = work.num1 * work.num2
  #   elif work.op == Operation.DIVIDE:
  #     if work.num2 == 0:
  #       x = InvalidOperation()
  #       x.what = work.op
  #       x.why = 'Cannot divide by 0'
  #       raise x
  #     val = work.num1 / work.num2
  #   else:
  #     x = InvalidOperation()
  #     x.what = work.op
  #     x.why = 'Invalid operation'
  #     raise x

  #   log = SharedStruct()
  #   log.key = logid
  #   log.value = '%d' % (val)
  #   self.log[logid] = log

  #   return val

  # def getStruct(self, key):
  #   print 'getStruct(%d)' % (key)
  #   return self.log[key]

  # def zip(self):
  #   print 'zip()'



def serve(port, db_path): 

  handler = ThriftVtorHandler(db_path)
  processor = ThriftVtor.Processor(handler)
  transport = TSocket.TServerSocket(port=port)
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


  # You could do one of these for a multithreaded server
  #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
  #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

  print 'Starting the server...'
  server.serve()
  print 'done.'