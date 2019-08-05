FROM golang:1.12
ENV GO111MODULE=on
WORKDIR /go/src/github.com/stephenhillier/apidash/monitor/
ADD go.* /go/src/github.com/stephenhillier/apidash/monitor/
RUN go get ./...
ADD . /go/src/github.com/stephenhillier/apidash/monitor/
RUN go install
ENTRYPOINT [ "/go/bin/monitor" ]
