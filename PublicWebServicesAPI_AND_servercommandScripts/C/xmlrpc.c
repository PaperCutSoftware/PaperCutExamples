// Call the PaperCut XML-RPC web services API
//
// Alec Clews <alec.clews@papercut.com>
//
// Adapted from
// https://sourceforge.net/p/xmlrpc-c/code/HEAD/tree/trunk/examples/xmlrpc_sample_add_client.c
//


#include <stdlib.h>
#include <xmlrpc-c/base.h>
#include <xmlrpc-c/client.h>

//#include "config.h" // supplied by your environment

#define NAME "PaperCut web services API XML-RPC C Test Client"
#define VERSION "0.1"


static void 
die_if_fault_occurred (xmlrpc_env * const envP) {
    if (envP->fault_occurred) {
        fprintf(stderr, "ERROR: %s (%d)\n",
                envP->fault_string, envP->fault_code);
        exit(1);
    }
}

int 
main(int           const argc, 
     const char ** const argv) {

    if (argc != 2) {
      fprintf(stderr, "ERROR: Must provide user name as paramter");
      exit (1);
    }

    char * const auth = "token";

    xmlrpc_env env;
    xmlrpc_client * clientP;
    xmlrpc_value * resultP;
    int found;
    char * const url = "http://localhost:9191/rpc/api/xmlrpc";

    char * const methodName = "api.isUserExists";

    /* Initialize our error-handling environment. */
    xmlrpc_env_init(&env);

    xmlrpc_client_setup_global_const(&env);

    xmlrpc_client_create(&env, XMLRPC_CLIENT_NO_FLAGS, NAME, VERSION, NULL, 0,
                         &clientP);
    die_if_fault_occurred(&env);

    /* Make the remote procedure call */
    xmlrpc_client_call2f(&env, clientP, url, methodName, &resultP,
                "(ss)", auth, argv[1]);
    die_if_fault_occurred(&env);
    
    /* Get our result and print it out. */
    xmlrpc_read_bool(&env, resultP, &found);
    die_if_fault_occurred(&env);
    printf("The user %s %s\n", argv[1], found? "exists": "does not exist");
    
    /* Dispose of our result value. */
    xmlrpc_DECREF(resultP);

    /* Clean up our error-handling environment. */
    xmlrpc_env_clean(&env);
    
    xmlrpc_client_destroy(clientP);

    xmlrpc_client_teardown_global_const();

    return 0;
}

