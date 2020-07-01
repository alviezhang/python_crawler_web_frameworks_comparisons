package main

import (
	"fmt"
	"net/http"
	"runtime"
	"strconv"
	"time"
)

func main() {
	runtime.GOMAXPROCS(1)
	http.HandleFunc("/", HelloServer)
	err := http.ListenAndServe(":8090", nil)
	if err != nil {
		fmt.Println("Failed to start server")
	}
}

func HelloServer(w http.ResponseWriter, r *http.Request) {
	var seconds float64
	keys, ok := r.URL.Query()["seconds"]
	if !ok {
		seconds = 0
	} else {
		_seconds, err := strconv.ParseFloat(keys[0], 32)
		if err != nil {
			seconds = 0
		} else {
			seconds = _seconds
		}
	}
	time.Sleep(time.Duration(seconds) * time.Second)
	fmt.Fprintf(w, "Sleep %f seconds", seconds)
}
