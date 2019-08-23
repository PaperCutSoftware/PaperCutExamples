// A PaperCut MG/NG user directory source
package main

// Build
//  go get github.com/divan/gorilla-xmlrpc/xml
//  go build cust-auth-sync.go

// Install:
// Copy the cust-auth-sync binary to [papercut install dir]/server/custom/local

// Config
// In the PaperCut MF/NG admin interface select
//  [options] -> [User/Group Sync]. Under [Primary Sync Source] set these values

//  [Primary sync source]  => [Custom Program ....]
//  [Custom user program]  => [C:\Program Files\PaperCut MF\server\custom\local\cust-auth-sync.exe]
//  [Custom auth program]  => [C:\Program Files\PaperCut MF\server\custom\local\cust-auth-sync.exe]

// Note modify the path and name of the binary depending on your platform

// This is a demo program so it comes with a default sample database. The
// 1st time the program is run it will create a json file with the sample
// data. Edit this file at any time to change the user and group databases,
// and the web services API token.

// Note after copying the binary
// into the [papercut install dir]/server/custom/local directory, but before
// performing the 1st user sync you can create the sample database and then
// edit the data. run the command
//     [papercut install dir]/server/custom/local/cust-auth-sync - is-valid

// This will create the database in [papercut install dir]/server/custom/local/config.json

// Note: This program assumes the advanced config key user-source.update-user-details-card-id
// is set to "Y"

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/divan/gorilla-xmlrpc/xml"
)

// Stuff to call the PaperCut web services API over XML-RPC

type client struct {
	uri       string
	port      string
	authToken string
}

// Make the RPC call
func xmlRpcCall(c client, method string, args interface{}, reply interface{}) error {
	buf, _ := xml.EncodeClientRequest(method, args)
	response, err := http.Post(c.uri+":"+c.port+"/rpc/api/xmlrpc", "text/xml", bytes.NewBuffer(buf))
	if err != nil {
		return err
	}
	defer response.Body.Close() // Can't defer until we know we have a response
	err = xml.DecodeClientResponse(response.Body, reply)
	return err
}

func (c client) getConfigValue(keyName string) (string, error) {
	var args interface{}

	args = &struct {
		Auth    string
		KeyName string
	}{
		c.authToken,
		keyName,
	}

	var reply struct{ ReturnValue string }
	err := xmlRpcCall(c, "api.getConfigValue", args, &reply)
	return reply.ReturnValue, err
}

func getConfigValue(token string, configName string) string {
	papercutServer := "http://localhost"
	papercutPort := "9191"

	r, err := client{papercutServer, papercutPort, token}.getConfigValue(configName)

	if err == nil {
		return r
	}

	fmt.Fprintln(os.Stderr, "Cannot use web services API. Please configure", err)
	return ""
}

func areUserNameAliasesEnabled(token string) (ret bool) {

	r := getConfigValue(token, "secondary-user-name.enabled")

	if len(r) > 0 {
		if r != "N" {
			fmt.Fprintln(os.Stderr, "PaperCut MF/NG is configured for secondary usernames (aliases)")
			return true
		} else {
			fmt.Fprintln(os.Stderr, "PaperCut MF/NG is NOT configured for secondary usernames (aliases)")
		}
	}
	return false
}

// End of web services helper

type userDBT map[string]userAttributesT

type userAttributesT struct {
	Fullname        string `json:"fullname"`
	Email           string `json:"email"`
	Dept            string `json:"dept"`
	Office          string `json:"office"`
	PrimaryCardno   string `json:"primarycardno"`
	OtherEmail      string `json:otheremail`
	SecondaryCardno string `json:secondarycardno`
	UserAlias       string `json:useralias`
	HomeDirectory   string `json:homedirectory`
	PIN             string `json:pin`
	Password        string `json:"password"`
}

type userDataT struct {
	Username string `json:"username"`
	userAttributesT
}

func (db userDBT) saveUser(userData userDataT) (err error) {
	if _, found := db.findUser(userData.Username); found {
		return fmt.Errorf("Duplicate user. Can't insert %v", userData.Username)
	}
	db[userData.Username] = userData.userAttributesT
	return nil
}

func (db userDBT) findUser(userName string) (userData userDataT, userFound bool) {
	for user, attributes := range db {
		if userName == user {
			return userDataT{
				Username:        user,
				userAttributesT: attributes}, true
		}
	}
	return userDataT{}, false
}

var userAliasConfigured bool

func (user userDataT) String() string {

	userAlias := ""

	if userAliasConfigured {
		userAlias = user.UserAlias
	}

	return fmt.Sprintf("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s",
		user.Username,
		user.Fullname,
		user.Email,
		user.Dept,
		user.Office,
		user.PrimaryCardno,
		user.OtherEmail,
		user.SecondaryCardno,
		userAlias,
		user.HomeDirectory,
		user.PIN,
	)
	// Don't return the user Password -- it's meant to be a secret!
}

type configT struct {
	WebServicesToken string              `json:auth.webservices.auth-token`
	UDB              userDBT             `json:"userdata"`
	GDB              map[string][]string `json:"groupdata"`
}

// Create some sample data and save it to disk
func saveConfig(filename string) (string, userDBT, map[string][]string, error) {

	fmt.Fprintf(os.Stderr, "Creating new default user and group database in %v\n", filename)
	userDB := make(userDBT)
	groupDB := make(map[string][]string)

	userDB.saveUser(userDataT{Username: "john", userAttributesT: userAttributesT{Fullname: "John Smith", Email: "johns@here.com", Dept: "Accounts", Office: "Melbourne", PrimaryCardno: "1234", OtherEmail: "personal1@webmail.com", SecondaryCardno: "01234", UserAlias: "user1", HomeDirectory: "\\\\server\\dfs\\homedirs\\user1", PIN: "1234", Password: "password1"}})
	userDB.saveUser(userDataT{Username: "jane", userAttributesT: userAttributesT{Fullname: "Jane Rodgers", Email: "janer@here.com", Dept: "Sales", Office: "Docklands", PrimaryCardno: "5678", OtherEmail: "personal2@webmail.com", SecondaryCardno: "05678", UserAlias: "user2", HomeDirectory: "\\\\server\\dfs\\homedirs\\user2", PIN: "1234", Password: "password2"}})
	userDB.saveUser(userDataT{Username: "ahmed", userAttributesT: userAttributesT{Fullname: "Ahmed Yakubb", Email: "ahmedy@here.com", Dept: "Marketing", Office: "Home Office", PrimaryCardno: "4321", OtherEmail: "personal2@webmail.com", SecondaryCardno: "04321", UserAlias: "user3", HomeDirectory: "\\\\server\\dfs\\homedirs\\user3", PIN: "1234", Password: "password3"}})

	groupDB["groupA"] = []string{"john"}
	groupDB["groupB"] = []string{"jane", "ahmed"}

	token := "change-me"

	c := configT{token, userDB, groupDB}

	bytes, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		return token, userDBT{}, map[string][]string{}, err
	}

	return token, userDB, groupDB, ioutil.WriteFile(filename, bytes, 0644)
}

// Read user and group database from disk
func getConfig() (token string, udb userDBT, gdb map[string][]string, err error) {

	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		log.Fatal(err)
	}

	filename := filepath.FromSlash(fmt.Sprintf("%v/%v", dir, "config.json"))

	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Could not read config file %v\n", err)
		token, udb, gdb, err := saveConfig(filename)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
		return token, udb, gdb, err
	}

	var c configT
	err = json.Unmarshal(bytes, &c)
	if err != nil {
		return token, userDBT{}, map[string][]string{}, err
	}

	return c.WebServicesToken, c.UDB, c.GDB, nil
}

func main() {

	token, userDB, groupDB, err := getConfig()

	if err != nil {
		fmt.Fprintln(os.Stderr, "config error")
		os.Exit(-1)
	}

	if len(os.Args) == 1 {
		var userName, password string

		fmt.Scan(&userName, &password)

		user, userFound := userDB.findUser(userName)

		if userFound && user.Password == password {
			fmt.Printf("OK\n%s\n", user.Username)
			os.Exit(0)
		}

		fmt.Fprintln(os.Stderr, "Wrong Username or Password")
		fmt.Println("ERROR")
		os.Exit(-1)
	}

	if len(os.Args) == 2 || os.Args[1] != "-" {
		fmt.Fprintf(os.Stderr, "Incorrect arguments passed: %v\n", os.Args[1:])
		os.Exit(-1)
	}

	userAliasConfigured = areUserNameAliasesEnabled(token)

	if os.Args[2] == "is-valid" {
		fmt.Println("Y")
		os.Exit(0)
	}

	if os.Args[2] == "all-users" {
		for user := range userDB {
			userdata, _ := userDB.findUser(user)
			fmt.Println(userdata)
		}
		os.Exit(0)
	}

	if os.Args[2] == "all-groups" {
		for g := range groupDB {
			fmt.Println(g)
		}
		os.Exit(0)
	}

	if os.Args[2] == "get-user-details" {
		var userName string
		fmt.Scan(&userName)
		if user, userFound := userDB.findUser(userName); userFound {
			fmt.Println(user)
			os.Exit(0)
		}
		fmt.Fprintf(os.Stderr, "Can't find user %s", userName)
		os.Exit(-1)
	}

	if os.Args[2] == "group-member-names" ||
		os.Args[2] == "group-members" ||
		os.Args[2] == "is-user-in-group" {

		if len(os.Args) < 4 {
			fmt.Fprintln(os.Stderr, "group info request -- no group name supplied")
			os.Exit(-1)
		}

		if os.Args[2] == "is-user-in-group" && len(os.Args) < 5 {
			fmt.Fprintln(os.Stderr, "is-user-in-group -- no user name supplied")
			os.Exit(-1)
		}

		for g, members := range groupDB {
			if g == os.Args[3] {
				for _, member := range members {
					if os.Args[2] == "group-members" {
						u, _ := userDB.findUser(member)
						fmt.Println(u)
					} else if os.Args[2] == "group-member-names" {
						fmt.Println(member)
					} else { //"is-user-in-group"
						if member == os.Args[4] {
							fmt.Println("Y")
							os.Exit(0)
						}
					}
				}
				if os.Args[2] == "is-user-in-group" {
					fmt.Println("N")
					os.Exit(-1)
				}
				os.Exit(0)
			}
		}
		fmt.Fprintln(os.Stderr, "Group not found")
		os.Exit(-1)
	}

	fmt.Fprintln(os.Stderr, "Can't process arguments", os.Args[1:])
	os.Exit(-1)
}
