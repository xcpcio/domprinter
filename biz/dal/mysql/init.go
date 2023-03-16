package mysql

import (
	"fmt"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

func Init() {
	var err error

	var mysql_hostname = os.Getenv("MYSQL_HOSTNAME")
	var mysql_port = os.Getenv("MYSQL_PORT")
	var mysql_username = os.Getenv("MYSQL_USERNAME")
	var mysql_password = os.Getenv("MYSQL_PASSWORD")
	var mysql_schema = os.Getenv("MYSQL_SCHEMA")

	var dsn = fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8&parseTime=True&loc=Local",
		mysql_username,
		mysql_password,
		mysql_hostname,
		mysql_port,
		mysql_schema,
	)

	DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		SkipDefaultTransaction: true,
		PrepareStmt:            true,
		Logger:                 logger.Default.LogMode(logger.Info),
	})

	if err != nil {
		panic(err)
	}
}
