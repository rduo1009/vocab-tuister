// Code generated by mkunion. DO NOT EDIT.
package workflow

import (
	"github.com/widmogrod/mkunion/x/machine"
	"github.com/widmogrod/mkunion/x/schema"
	"github.com/widmogrod/mkunion/x/shared"
	"github.com/widmogrod/mkunion/x/storage/schemaless"
	"strings"
	"testing"
)

func init() {
	shared.TypeRegistryStore[machine.Case[Dependency, Command, State]]("github.com/widmogrod/mkunion/x/machine.Case[github.com/widmogrod/mkunion/x/workflow.Dependency,github.com/widmogrod/mkunion/x/workflow.Command,github.com/widmogrod/mkunion/x/workflow.State]")
	shared.TypeRegistryStore[machine.Machine[Dependency, Command, State]]("github.com/widmogrod/mkunion/x/machine.Machine[github.com/widmogrod/mkunion/x/workflow.Dependency,github.com/widmogrod/mkunion/x/workflow.Command,github.com/widmogrod/mkunion/x/workflow.State]")
	shared.TypeRegistryStore[schema.Binary]("github.com/widmogrod/mkunion/x/schema.Binary")
	shared.TypeRegistryStore[schema.Bool]("github.com/widmogrod/mkunion/x/schema.Bool")
	shared.TypeRegistryStore[schema.List]("github.com/widmogrod/mkunion/x/schema.List")
	shared.TypeRegistryStore[schema.Map]("github.com/widmogrod/mkunion/x/schema.Map")
	shared.TypeRegistryStore[schema.None]("github.com/widmogrod/mkunion/x/schema.None")
	shared.TypeRegistryStore[schema.Number]("github.com/widmogrod/mkunion/x/schema.Number")
	shared.TypeRegistryStore[schema.String]("github.com/widmogrod/mkunion/x/schema.String")
	shared.TypeRegistryStore[schemaless.Record[State]]("github.com/widmogrod/mkunion/x/storage/schemaless.Record[github.com/widmogrod/mkunion/x/workflow.State]")
	shared.TypeRegistryStore[strings.Builder]("strings.Builder")
	shared.TypeRegistryStore[testing.T]("testing.T")
	shared.TypeRegistryStore[And]("github.com/widmogrod/mkunion/x/workflow.And")
	shared.TypeRegistryStore[Apply]("github.com/widmogrod/mkunion/x/workflow.Apply")
	shared.TypeRegistryStore[ApplyAwaitOptions]("github.com/widmogrod/mkunion/x/workflow.ApplyAwaitOptions")
	shared.TypeRegistryStore[Assign]("github.com/widmogrod/mkunion/x/workflow.Assign")
	shared.TypeRegistryStore[Await]("github.com/widmogrod/mkunion/x/workflow.Await")
	shared.TypeRegistryStore[BaseState]("github.com/widmogrod/mkunion/x/workflow.BaseState")
	shared.TypeRegistryStore[Callback]("github.com/widmogrod/mkunion/x/workflow.Callback")
	shared.TypeRegistryStore[Choose]("github.com/widmogrod/mkunion/x/workflow.Choose")
	shared.TypeRegistryStore[Compare]("github.com/widmogrod/mkunion/x/workflow.Compare")
	shared.TypeRegistryStore[DI]("github.com/widmogrod/mkunion/x/workflow.DI")
	shared.TypeRegistryStore[DelayRun]("github.com/widmogrod/mkunion/x/workflow.DelayRun")
	shared.TypeRegistryStore[Done]("github.com/widmogrod/mkunion/x/workflow.Done")
	shared.TypeRegistryStore[End]("github.com/widmogrod/mkunion/x/workflow.End")
	shared.TypeRegistryStore[Error]("github.com/widmogrod/mkunion/x/workflow.Error")
	shared.TypeRegistryStore[ExpireAsync]("github.com/widmogrod/mkunion/x/workflow.ExpireAsync")
	shared.TypeRegistryStore[Flow]("github.com/widmogrod/mkunion/x/workflow.Flow")
	shared.TypeRegistryStore[FlowRef]("github.com/widmogrod/mkunion/x/workflow.FlowRef")
	shared.TypeRegistryStore[FunctionInput]("github.com/widmogrod/mkunion/x/workflow.FunctionInput")
	shared.TypeRegistryStore[FunctionOutput]("github.com/widmogrod/mkunion/x/workflow.FunctionOutput")
	shared.TypeRegistryStore[GetValue]("github.com/widmogrod/mkunion/x/workflow.GetValue")
	shared.TypeRegistryStore[NextOperation]("github.com/widmogrod/mkunion/x/workflow.NextOperation")
	shared.TypeRegistryStore[Not]("github.com/widmogrod/mkunion/x/workflow.Not")
	shared.TypeRegistryStore[Or]("github.com/widmogrod/mkunion/x/workflow.Or")
	shared.TypeRegistryStore[ResumeOptions]("github.com/widmogrod/mkunion/x/workflow.ResumeOptions")
	shared.TypeRegistryStore[ResumeSchedule]("github.com/widmogrod/mkunion/x/workflow.ResumeSchedule")
	shared.TypeRegistryStore[Run]("github.com/widmogrod/mkunion/x/workflow.Run")
	shared.TypeRegistryStore[ScheduleRun]("github.com/widmogrod/mkunion/x/workflow.ScheduleRun")
	shared.TypeRegistryStore[ScheduleStopped]("github.com/widmogrod/mkunion/x/workflow.ScheduleStopped")
	shared.TypeRegistryStore[Scheduled]("github.com/widmogrod/mkunion/x/workflow.Scheduled")
	shared.TypeRegistryStore[SetValue]("github.com/widmogrod/mkunion/x/workflow.SetValue")
	shared.TypeRegistryStore[StopSchedule]("github.com/widmogrod/mkunion/x/workflow.StopSchedule")
	shared.TypeRegistryStore[ToStrContext]("github.com/widmogrod/mkunion/x/workflow.ToStrContext")
	shared.TypeRegistryStore[TryRecover]("github.com/widmogrod/mkunion/x/workflow.TryRecover")
}