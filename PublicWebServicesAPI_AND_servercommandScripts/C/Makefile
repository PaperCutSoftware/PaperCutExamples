PROJECT:=xmlrpc
	
XMLRPC_FLAGS:=${shell xmlrpc-c-config client --cflags --libs}

CFLAGS+=$(XMLRPC_FLAGS)

$(PROJECT): $(PROJECT).c
