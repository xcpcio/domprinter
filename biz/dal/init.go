package dal

import (
	"github.com/Dup4/domprinter/biz/dal/mysql"
	"github.com/Dup4/domprinter/biz/model/query"
)

func init() {
	mysql.Init()
	query.SetDefault(mysql.DB)
}
