namespace go domprinter

enum RespCodeEnum {
    Success = 0,
    ParamInvalid = 1,
    DBErr = 2,
}

struct BaseResp {
    1: RespCodeEnum RespCode,
    2: string RespMessage,
}

enum TaskStateEnum {
    Unknown = 0,

    Submitted = 1,
    Completed = 2,
    Abandoned = 3,
}

struct PrintTaskDTO {
    1: string SubmitTime,
    2: string UserName,
    3: string TeamName,
    4: string TeamID,
    5: string Location,
    6: string Language,
    7: string FileName,
    8: string SourceCode,

    9: optional i64 PrintTaskID,
    10: required TaskStateEnum TaskState = TaskStateEnum.Unknown,
}

struct FetchPrintTaskReq {
    1: TaskStateEnum TaskState,
    2: optional i64 OffsetTaskID,
    3: optional i64 LimitTaskNum,
}

struct FetchPrintTaskResp {
    1: list<PrintTaskDTO> PrintTaskList,
    2: BaseResp BaseResp,
}

struct SubmitPrintTaskReq {
    1: PrintTaskDTO PrintTask,
}

struct SubmitPrintTaskResp {
    1: i64 PrintTaskID,
    2: BaseResp BaseResp,
}

struct UpdatePrintTaskReq {
    1: list<i64> PrintTaskIDList,
    2: TaskStateEnum TaskState,
}

struct UpdatePrintTaskResp {
    1: BaseResp BaseResp,
}

service DOMPrinterService {
    FetchPrintTaskResp FetchPrintTask(1: FetchPrintTaskReq request) (api.get = "/print-task"),
    SubmitPrintTaskResp SubmitPrintTask(1: SubmitPrintTaskReq request) (api.post = "/print-task"),
    UpdatePrintTaskResp UpdatePrintTask(1: UpdatePrintTaskReq request) (api.patch = "/print-task"),
}
