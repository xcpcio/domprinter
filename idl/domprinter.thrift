namespace go domprinter

struct BaseResp {
    1: i32 StatusCode,
    2: string StatusMessage,
}

enum TaskStateEnum {
    Submitted = 0,
    Completed = 1,
    Abandoned = 2,
    Unknown = 255,
}

struct PrintTaskBody {
    1: i64 Timestamp,
    2: string UserName,
    3: string TeamName,
    4: string TeamID,
    5: string Location,
    6: string Language,
    7: string FileName,
    8: string SourceCode,
}

struct PrintTaskDTO {
    1: i64 PrintTaskID,
    2: TaskStateEnum TaskState,
    3: PrintTaskBody PrintTaskBody,
}

struct FetchPrintTaskReq {
    1: TaskStateEnum TaskState,
    2: optional i64 StartTaskID,
    3: optional i64 TaskNumLimit,
}

struct FetchPrintTaskResp {
    1: list<PrintTaskBody> PrintTaskBodyList,
    2: BaseResp BaseResp,
}

struct SubmitPrintTaskReq {
    1: PrintTaskBody PrintTaskBody,
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
