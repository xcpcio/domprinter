package main

import (
	"github.com/Dup4/domprinter/biz/dal/mysql"
	genModel "github.com/Dup4/domprinter/biz/model/orm_gen"

	"gorm.io/gen"

	_ "github.com/Dup4/domprinter/biz/dal"
)

func main() {
	g := gen.NewGenerator(gen.Config{
		OutPath:      "./biz/model/query",
		ModelPkgPath: "./biz/model/orm_gen",
		Mode:         gen.WithDefaultQuery | gen.WithQueryInterface,
	})

	mysql.Init()

	g.UseDB(mysql.DB)
	g.GenerateModel("print_task")

	g.ApplyBasic(genModel.PrintTask{})

	g.Execute()
}
