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

// Edit to suit -- helps PaperCut admin know what this is for
const tokenName = "integration-auth"

var cmdBin string

func init() {

	var installRoot string

	if runtime.GOOS == "windows" {

		if _, err := os.Stat("C:\\Program Files\\PaperCut MF"); err == nil {
			installRoot = "C:\\Program Files\\PaperCut MF"
		} else if _, err := os.Stat("C:\\Program Files\\PaperCut NG"); err == nil {
			installRoot = "C:\\Program Files\\PaperCut NG"
		} else {
			log.Fatal("PaperCut MF/NG installation not found")
		}
		cmdBin = filepath.Join(installRoot, "server", "bin", "win", "server-command.exe")

	} else if runtime.GOOS == "linux" {
		if papercutAdmin, err := user.Lookup("papercut"); err != nil {
			log.Fatal("PaperCut not installed")
		} else {
			installRoot := papercutAdmin.HomeDir
			if _, err := os.Stat(installRoot); err != nil {
				log.Fatal("PaperCut not installed")
			}

			cmdBin = filepath.Join(installRoot, "server", "bin", "linux_x64", "server-command")
		}
	} else if runtime.GOOS == "darwin" {
		if _, err := os.Stat("/Applications/PaperCut MF"); err == nil {
			installRoot = "/Applications/PaperCut MF"
		} else if _, err := os.Stat("/Applications/PaperCut NG"); err == nil {
			installRoot = "/Applications/PaperCut NG"
		} else {
			log.Fatal("PaperCut not installed")
		}
		cmdBin = filepath.Join(installRoot, "server", "bin", "macos", "server-command")
	} else {
		log.Fatalf("Runtime platform %v not supported", runtime.GOOS)
	}
}

// Note: using server-command binary as we don't know have a value web services auth token yet
func getConfig(key string) (value []byte, err error) {
	cmd := exec.Command(cmdBin, "get-config", key)
	var out bytes.Buffer
	cmd.Stdout = &out
	log.Printf("Running command %v and waiting for it to finish...", cmdBin)
	err = cmd.Run()
	value = []byte(strings.TrimSpace(out.String()))
	return value, err
}

func setConfig(key string, value string) (err error) {
	cmd := exec.Command(cmdBin, "set-config", key, value)
	var out bytes.Buffer
	cmd.Stdout = &out
	log.Printf("Running command %v and waiting for it to finish... (setting %v to %v", cmdBin, key, value)
	err = cmd.Run()
	return err
}

func main() {

	var result []byte
	var err error

	if len(os.Args) == 1 {
		log.Fatal("Auth key value not supplied")
	}

	securityToken := os.Args[1]

	if result, err = getConfig("auth.webservices.auth-token"); err != nil {
		log.Fatalf("Failed getConfig result=%v, err = %v", result, err)
	}

	log.Printf("result: %q", result)

	if len(result) == 0 {

		auth := make(map[string]string)
		auth[tokenName] = securityToken

		if value, err := json.Marshal(auth); err != nil {
			log.Fatalf("could not marshal %v", auth)
		} else {
			setConfig("auth.webservices.auth-token", string(value))
			fmt.Printf("Updated with new token value %v", auth)
			return
		}
	}

	if json.Valid(result) != true {
		log.Printf("auth.webservices.auth-token is a simple string")

		tokensAsObject := make(map[string]string)
		tokensAsObject[tokenName] = securityToken
		tokensAsObject["default"] = string(result)

		if value, err := json.Marshal(tokensAsObject); err != nil {
			log.Fatalf("could not marshal %v", tokensAsObject)
		} else {
			setConfig("auth.webservices.auth-token", string(value))
			fmt.Printf("Updated with new token value %v", string(value))
			return
		}
	}

	var tokensAsObject map[string]string

	if err := json.Unmarshal(result, &tokensAsObject); err == nil {
		fmt.Printf("auth.webservices.auth-token is a json object %v", tokensAsObject)

		tokensAsObject[tokenName] = securityToken
		if value, err := json.Marshal(tokensAsObject); err != nil {
			log.Fatalf("could not marshal %v", tokensAsObject)
		} else {
			setConfig("auth.webservices.auth-token", string(value))
			fmt.Printf("Updated with new token value %v", string(value))
			return
		}
	}
	var tokensAsArray []string

	// Note: if the config key is not an array of strings this parse will fail
	if err := json.Unmarshal(result, &tokensAsArray); err == nil {
		log.Printf("auth.webservices.auth-token is a json array %v", tokensAsArray)

		for _, i := range tokensAsArray {
			if i == securityToken {
				log.Printf("Security token %v already installed", i)
				return
			}
		}

		if value, err := json.Marshal(append(tokensAsArray, securityToken)); err != nil {
			log.Fatalf("could not marshal %v", append(tokensAsArray, securityToken))
		} else {
			setConfig("auth.webservices.auth-token", string(value))
			fmt.Printf("Updated with new token value %v", string(value))
			return
		}
	}

	log.Fatal("Cannot parse setting")
}
