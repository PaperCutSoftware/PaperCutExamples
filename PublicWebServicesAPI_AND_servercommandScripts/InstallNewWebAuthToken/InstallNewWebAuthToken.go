package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"runtime"
	"strings"
)

var serverCommandBin string

// Before we do anything let's find the localtion of the server-command binary
func init() {

	var installRoot string

	if runtime.GOOS == "windows" {

		programFiles := os.Getenv("PROGRAMFILES")

		installRoot := fmt.Sprintf("%s\\PaperCut MF", programFiles)
		if _, err := os.Stat(installRoot); err != nil {

			installRoot = fmt.Sprintf("%s\\PaperCut NG", programFiles)

			if _, err := os.Stat(fmt.Sprintf("%s\\PaperCut NG", programFiles)); err != nil {
				log.Fatal("PaperCut MF/NG installation not found")
			}
		}

		serverCommandBin = filepath.Join(installRoot, "server", "bin", "win", "server-command.exe")

	} else if runtime.GOOS == "linux" {
		if papercutAdmin, err := user.Lookup("papercut"); err != nil {
			log.Fatal("PaperCut not installed")
		} else {
			installRoot := papercutAdmin.HomeDir
			if _, err := os.Stat(installRoot); err != nil {
				log.Fatal("PaperCut not installed")
			}

			serverCommandBin = filepath.Join(installRoot, "server", "bin", "linux-x64", "server-command")
		}

	} else if runtime.GOOS == "darwin" {
		if _, err := os.Stat("/Applications/PaperCut MF"); err == nil {
			installRoot = "/Applications/PaperCut MF"
		} else if _, err := os.Stat("/Applications/PaperCut NG"); err == nil {
			installRoot = "/Applications/PaperCut NG"
		} else {
			log.Fatal("PaperCut not installed")
		}
		serverCommandBin = filepath.Join(installRoot, "server", "bin", "macos", "server-command")
	} else {
		log.Fatalf("Runtime platform %v not supported", runtime.GOOS)
	}
}

// Note: using server-command binary as we don't know have a value web services auth token yet
func execServerCommand(args ...string) (value []byte, err error) {

	var out bytes.Buffer

	cmd := exec.Command(serverCommandBin, args...)
	cmd.Stdout = &out
	log.Printf("Running command %v and waiting for it to finish...", append([]string{serverCommandBin}, args...))

	err = cmd.Run()
	value = []byte(strings.TrimSpace(out.String()))

	return
}

func update(jsonData interface{}) {
	if value, err := json.Marshal(jsonData); err != nil {
		log.Fatalf("could not marshal %v", jsonData)
	} else {
		if output, err := execServerCommand("set-config", "auth.webservices.auth-token", string(value)); err != nil {
			log.Fatalf("Failed to update auth.webservices.auth-token: %v", output)
		}
		log.Printf("Updated auth.webservices.auth-token with new token value %v", value)
	}
}

func main() {

	var result []byte
	var err error

	if len(os.Args) != 3 {
		log.Fatal("Auth key and value not supplied")
	}

	tokenName := os.Args[1]
	securityToken := os.Args[2]

	log.Printf("Adding key %v, value %v", tokenName, securityToken)

	if result, err = execServerCommand("get-config", "auth.webservices.auth-token"); err != nil {
		log.Fatalf("Failed getConfig result=%v, err = %v", result, err)
	}

	if len(result) == 0 {

		auth := make(map[string]string)
		auth[tokenName] = securityToken

		update(auth)

		return
	}

	var tokensAsArray []string

	// Note: if the config key is not an array of strings this parse will fail
	if notAnArray := json.Unmarshal(result, &tokensAsArray); notAnArray == nil {
		log.Printf("auth.webservices.auth-token is a json array %v", tokensAsArray)

		for _, i := range tokensAsArray {
			if i == securityToken {
				log.Printf("Security token %v already installed", i)
				return
			}
		}

		update(append(tokensAsArray, securityToken))
		return
	}

	var tokensAsObject map[string]string

	// Note: if the config key is not a map of strings indexed by strings this parse will fail
	if notAnObject := json.Unmarshal(result, &tokensAsObject); notAnObject == nil {
		log.Printf("auth.webservices.auth-token is a json object %v", tokensAsObject)

		tokensAsObject[tokenName] = securityToken

		update(tokensAsObject)

		return
	}

	// Assume it's a simple string
	log.Printf("auth.webservices.auth-token is a simple string")

	tokensAsObject = make(map[string]string)
	tokensAsObject["default"] = string(result) // Save the old auth key as well
	tokensAsObject[tokenName] = securityToken

	update(tokensAsObject)

	return
}
