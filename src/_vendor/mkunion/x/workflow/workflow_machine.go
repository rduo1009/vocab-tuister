package workflow

import (
	"github.com/widmogrod/mkunion/x/schema"
)

type StepID = string
type FlowID = string
type RunID = string

type Execution struct {
	FlowID    FlowID
	Status    State
	Location  string
	StartTime int64
	EndTime   int64
	Variables map[string]schema.Schema
}

//go:tag mkunion:"RunOption"
type (
	ScheduleRun struct {
		// CRON like definition
		Interval string
		// ParentRunID is a reference to the original run, that scheduled this run and any between
		// ParentRunID is used to track history of the execution, and is stable reference to the original run
		ParentRunID string
	}
	DelayRun struct {
		// DelayBySeconds
		DelayBySeconds int64
	}
)

//go:tag mkunion:"Command"
type (
	Run struct {
		Flow  Workflow
		Input schema.Schema
		// Schedule run
		RunOption RunOption
	}
	Callback struct {
		CallbackID string
		Result     schema.Schema
		//Fail       schema.Schema
	}
	TryRecover struct {
		RunID RunID
	}
	StopSchedule struct {
		// ParentRunID can be stopped by user, or by system
		ParentRunID RunID
	}
	ResumeSchedule struct {
		ParentRunID RunID
	}
	ExpireAsync struct {
		RunID RunID
	}
)

//go:tag mkunion:"State"
type (
	NextOperation struct {
		Result    schema.Schema
		BaseState BaseState
	}
	Done struct {
		Result    schema.Schema
		BaseState BaseState
	}
	Error struct {
		Code    string
		Reason  string
		Retried int64
		//MaxRetries int64
		BaseState BaseState
	}
	Await struct {
		CallbackID               string
		ExpectedTimeoutTimestamp int64
		BaseState                BaseState
	}
	// Scheduled is a state that is used to schedule execution of the flow, once or periodically
	Scheduled struct {
		// ExpectedRunTimestamp is server timestamp + DelayBySeconds
		ExpectedRunTimestamp int64

		BaseState BaseState
	}
	ScheduleStopped struct {
		BaseState BaseState
	}
)

//go:tag serde:"json"
type BaseState struct {
	Flow       Workflow // Flow is a reference to the flow that describes execution
	RunID      RunID    // RunID is a unique identifier of the execution
	StepID     StepID   // StepID is a unique identifier of the step in the execution
	Variables  map[string]schema.Schema
	ExprResult map[string]schema.Schema

	// Default values
	DefaultMaxRetries int64

	RunOption RunOption
}

const (
	ProblemVariableNameInUser  = "assign-variable"
	ProblemVariableAccess      = "execute-reshaper"
	ProblemMissingFunction     = "missing-function"
	ProblemExecutingFunction   = "function-execution"
	ProblemPredicateEvaluation = "choose-evaluate-predicate"
	ProblemChooseThenEmpty     = "choose-then-empty"
	ProblemCallbackTimeout     = "callback-timeout"
)

//go:tag mkunion:"Workflow"
type (
	Flow struct {
		Name string // name of the flow
		Arg  string // name of the argument, which will hold the input to the flow
		Body []Expr
	}
	FlowRef struct {
		FlowID string
	}
)

//go:tag mkunion:"Expr"
type (
	End struct {
		ID     StepID
		Result Reshaper
	}
	Assign struct {
		ID    StepID
		VarOk string
		// if VarErr is not empty, then error will be assigned to this variable
		// to give chance to handle it, before it will be returned to the caller
		// otherwise, any error will stop execution of the program
		VarErr string
		Val    Expr
	}
	Apply struct {
		ID    StepID
		Name  string
		Args  []Reshaper
		Await *ApplyAwaitOptions
	}
	Choose struct {
		ID   StepID
		If   Predicate
		Then []Expr
		Else []Expr
	}
	//// Try allows to define a rules to recover from error in certain expression block
	//// Concept of this expression is experimental and similar to try/catch in other languages.
	//// ```
	//// try {
	////   // do something
	//// } catch (e) {
	////   // handle error
	//// }
	////
	//// It could be replaced, with enforcing that error or success is always returned as value of function
	//// and then using Choose to decide what to do next.
	//// ```
	//// res = ReserveInventory(...)
	//// if res.ok {
	////   // do something
	//// } else {
	////   // handle error
	//// }
	////
	//// Alternatively, it could be replaced with let and if.
	//// Let has special property, that if second variable error is not defined, it will stop execution of program
	//// but if it is defined, it will continue execution, and problemw will be accessible as variable to handle
	//// ```
	//// let res, err = await ReserveInventory(...)
	//// if err {
	////   // handle error
	//// }
	//// // do something
	//// ```
	//Try struct {
	//	ID    string
	//	Try   []Expr
	//	Catch []Expr
	//}

	//// ResumeSchedule is like reverse callback, or Apply with await.
	//// ResumeSchedule waits for caller to provide a result, and then continue execution.
	//// ```
	//// 	let res, err = await ReserveInventory(...)
	//// 	if err {
	//// 		// timeout reached
	//// 		_ = CancelReservation(...)
	//// 		return({"status": "timeout"})
	////	}
	////
	//// let approved = await Int > 2
	//// let approved = await {name: String > 0 and // , age: Int > 0}
	//// if !approved {
	////   _ = CancelReservation(...)
	////   return({status: "rejected"})
	//// }
	////
	//ResumeSchedule struct {
	//	ID      string
	//	ExpectedTimeoutTimestamp time.DelayBySeconds
	//	//Caller  schema.Schema
	//	//Callee  schema.Schema
	//	RunOption ResumeOptions
	//}
)

//go:tag serde:"json"
type ResumeOptions struct {
	Timeout int64
	//ExpectedTimeoutTimestamp time.DelayBySeconds
}

//go:tag serde:"json"
type ApplyAwaitOptions struct {
	TimeoutSeconds int64
	//ExpectedTimeoutTimestamp time.DelayBySeconds
}

//go:tag mkunion:"Reshaper"
type (
	GetValue struct {
		Path string
	}
	SetValue struct {
		Value schema.Schema
	}
)

//go:tag mkunion:"Predicate"
type (
	And struct {
		L []Predicate
	}
	Or struct {
		L []Predicate
	}
	Not struct {
		P Predicate
	}
	Compare struct {
		Operation string
		Left      Reshaper
		Right     Reshaper
	}
)
