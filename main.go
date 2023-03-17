// Code generated by hertz generator.

package main

import (
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/hertz-contrib/requestid"
	"github.com/hertz-contrib/swagger"
	swaggerFiles "github.com/swaggo/files"

	"github.com/Dup4/domprinter/biz/dal"
	_ "github.com/Dup4/domprinter/swagger"
)

// @BasePath /
// @schemes http
func main() {
	dal.Init()

	h := server.Default()
	h.Use(requestid.New())

	register(h)

	h.GET("/swagger/*any", swagger.WrapHandler(swaggerFiles.Handler))

	h.Spin()
}
