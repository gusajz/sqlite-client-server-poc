/*
Hive like thrift protocol
*/

typedef string TSessionHandle

// A Boolean column value.
struct TBoolValue {
  // NULL if value is unset.
  1: optional bool value
}

// A signed, 32 bit column value
struct TI32Value {
  // NULL if value is unset
  1: optional i32 value
}

// A floating point 64 bit column value
struct TDoubleValue {
  // NULL if value is unset
  1: optional double value
}

struct TStringValue {
  // NULL if value is unset
  1: optional string value
}

union TColumnValue {
  1: TBoolValue   boolVal      // BOOLEAN
  4: TI32Value    i32Val       // INT
  6: TDoubleValue doubleVal    // FLOAT, DOUBLE
  7: TStringValue stringVal    // STRING, LIST, MAP, STRUCT, UNIONTYPE, BINARY, DECIMAL, NULL, INTERVAL_YEAR_MONTH, INTERVAL_DAY_TIME
}


// Represents a row in a rowset.
struct TRow {
  1: required list<TColumnValue> colVals
}
// ExecuteStatement()
//
// Execute a statement.
// The returned OperationHandle can be used to check on the
// status of the statement, and to fetch results once the
// statement has finished executing.
struct TExecuteStatementReq {
  1: required string statement
}

struct TExecuteStatementResp {
  1: required list<TRow> rows
}


exception TOperationalError {
    1: string message;
}

service ThriftVtor {

  #TOpenSessionResp OpenSession();

  #TCloseSessionResp CloseSession(1:TCloseSessionReq req);

  TExecuteStatementResp ExecuteStatement(1:TExecuteStatementReq req) throws (1:TOperationalError unavailable);

  #TGetSchemasResp GetSchemas(1:TGetSchemasReq req);

  #TGetTablesResp GetTables(1:TGetTablesReq req);

  #TGetTableTypesResp GetTableTypes(1:TGetTableTypesReq req);

  #TGetColumnsResp GetColumns(1:TGetColumnsReq req);

  #TGetFunctionsResp GetFunctions(1:TGetFunctionsReq req);

  #TGetOperationStatusResp GetOperationStatus(1:TGetOperationStatusReq req);
  
  #TCancelOperationResp CancelOperation(1:TCancelOperationReq req);

  #TCloseOperationResp CloseOperation(1:TCloseOperationReq req);

  #TGetResultSetMetadataResp GetResultSetMetadata(1:TGetResultSetMetadataReq req);

  #TFetchResultsResp FetchResults(1:TFetchResultsReq req);

  #TGetDelegationTokenResp GetDelegationToken(1:TGetDelegationTokenReq req);

  #TCancelDelegationTokenResp CancelDelegationToken(1:TCancelDelegationTokenReq req);

  #TRenewDelegationTokenResp RenewDelegationToken(1:TRenewDelegationTokenReq req);
}
