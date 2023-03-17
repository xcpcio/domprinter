package main

import (
	"context"
	"fmt"
	"os"

	"github.com/cloudwego/hertz/pkg/protocol/consts"

	"github.com/Dup4/domprinter/hertz_client/domprinter"
	"github.com/Dup4/domprinter/hertz_client/domprinter_service"
)

func main() {
	client, err := domprinter_service.NewDOMPrinterServiceClient("http://127.0.0.1:8888")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	req := domprinter.NewPingReq()
	resp, rawResp, err := client.Ping(context.Background(), req)
	if err != nil {
		fmt.Println(err)
		os.Exit(2)
	}

	if rawResp.StatusCode() == consts.StatusOK && resp.GetMessage() == "pong" {
		os.Exit(0)
	} else {
		fmt.Printf("Ping Failed. [StatusCode=%d]", rawResp.StatusCode())
		os.Exit(3)
	}
}
