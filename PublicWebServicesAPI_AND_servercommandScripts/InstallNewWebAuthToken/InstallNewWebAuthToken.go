package main

import (
	"bytes"
	"encoding/json"
	"log"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"runtime"
	"strings"
)

// Edit to suit -- helps PaperCut admin know what this is for

var serverCommandBin string

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
		serverCommandBin = filepath.Join(installRoot, "server", "bin", "win", "server-command.exe")

	} else if runtime.GOOS == "linux" {
		if papercutAdmin, err := user.Lookup("papercut"); err != nil {
			log.Fatal("PaperCut not installed")
		} else {
			installRoot := papercutAdmin.HomeDir
			if _, err := os.Stat(installRoot); err != nil {
				log.Fatal("PaperCut not installed")
			}

			serverCommandBin = filepath.Join(installRoot, "server", "bin", "linux_x64", "server-command")
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

func execServerCommand(args ...string) (value []byte, err error) {

	var out bytes.Buffer

	cmd := exec.Command(serverCommandBin, args...)
	cmd.Stdout = &out
	log.Printf("Running command %v and waiting for it to finish...", append([]string{serverCommandBin}, args...))

	err = cmd.Run()
	value = []byte(strings.TrimSpace(out.String()))

	return
}

// Note: using server-command binary as we don't know have a value web services auth token yet
func getConfig(key string) (value []byte, err error) {
	return execServerCommand("get-config", key)
}

func setConfig(key string, value string) (err error) {
	_, err = execServerCommand("set-config", key, value)
	return err
}

func update(jsonData interface{}) {
	if value, err := json.Marshal(jsonData); err != nil {
		log.Fatalf("could not marshal %v", jsonData)
	} else {
		setConfig("auth.webservices.auth-token", string(value))
		log.Printf("Updated with new token value %v", jsonData)
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

	if result, err = getConfig("auth.webservices.auth-token"); err != nil {
		log.Fatalf("Failed getConfig result=%v, err = %v", result, err)
	}

	log.Printf("result: %q", result)

	if len(result) == 0 {

		auth := make(map[string]string)
		auth[tokenName] = securityToken

		update(auth)

		return
	}

	var tokensAsObject map[string]string

	if json.Valid(result) != true {
		log.Printf("auth.webservices.auth-token is a simple string")

		tokensAsObject = make(map[string]string)
		tokensAsObject["default"] = string(result) // Save the old auth key as well
		tokensAsObject[tokenName] = securityToken

		update(tokensAsObject)

		return
	}

	if err := json.Unmarshal(result, &tokensAsObject); err == nil {
		log.Printf("auth.webservices.auth-token is a json object %v", tokensAsObject)

		tokensAsObject[tokenName] = securityToken

		update(tokensAsObject)

		return
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

		update(append(tokensAsArray, securityToken))

		return
	}

	log.Fatal("Cannot parse setting")
}
