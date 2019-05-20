// A PaperCut MG/NG user directory source
package main

// Build
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
// data. Edit this file at any time to change the user and group databases.

// Note if you don't want use the sample data, then after copying the binary
// into the [papercut install dir]/server/custom/local directory, but before
// performing the 1st user sync you can create the sample database and then
// edit the data. run the command
//     [papercut install dir]/server/custom/local/cust-auth-sync - is-valid

// This will create the database in [papercut install dir]/server/custom/local/config.json

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
)

type userDBT map[string]userAttributesT

type userAttributesT struct {
	Fullname string `json:"fullname"`
	Email    string `json:"email"`
	Dept     string `json:"dept"`
	Office   string `json:"office"`
	Cardno   string `json:"cardno"`
	Password string `json:"password"`
}

type userDataT struct {
	Username string `json:"username"`
	userAttributesT
}

func (db userDBT) findUser(userName string) (userData userDataT, userFound bool) {
	for user, attributes := range db {
		if userName == user {
			return userDataT{
				Username: user,
				userAttributesT: userAttributesT{
					Fullname: attributes.Fullname,
					Email:    attributes.Email,
					Dept:     attributes.Dept,
					Office:   attributes.Office,
					Cardno:   attributes.Cardno,
					Password: attributes.Password}}, true
		}
	}
	return userDataT{}, false
}

func (user userDataT) String() (userString string) {
	// Don't return the user Password -- it's meant to be a secret!
	return fmt.Sprintf("%s\t%s\t%s\t%s\t%s\t%s", user.Username, user.Fullname, user.Email, user.Dept, user.Office, user.Cardno)
}

type configT struct {
	UDB userDBT             `json:"userdata"`
	GDB map[string][]string `json:"groupdata"`
}

func saveConfig(filename string) (userDBT, map[string][]string, error) {

	fmt.Fprintf(os.Stderr, "Creating new default user and group database in %v\n", filename)
	userDB := make(userDBT)
	groupDB := make(map[string][]string)

	userDB["john"] = userAttributesT{Fullname: "John Smith", Email: "johns@here.com", Dept: "Accounts", Office: "Melbourne", Cardno: "1234", Password: "password1"}
	userDB["jane"] = userAttributesT{Fullname: "Jane Rodgers", Email: "janer@here.com", Dept: "Sales", Office: "Docklands", Cardno: "5678", Password: "password2"}
	userDB["ahmed"] = userAttributesT{Fullname: "Ahmed Yakubb", Email: "ahmedy@here.com", Dept: "Marketing", Office: "Home Office", Cardno: "4321", Password: "password3"}

	groupDB["groupA"] = []string{"john"}
	groupDB["groupB"] = []string{"jane", "ahmed"}

	c := configT{userDB, groupDB}

	bytes, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		return userDBT{}, map[string][]string{}, err
	}

	return userDB, groupDB, ioutil.WriteFile(filename, bytes, 0644)
}

func getConfig() (udb userDBT, gdb map[string][]string, err error) {

	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		log.Fatal(err)
	}

	filename := filepath.FromSlash(fmt.Sprintf("%v/%v", dir, "config.json"))

	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Could not read config file %v\n", err)
		udb, gdb, err := saveConfig(filename)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
		return udb, gdb, err
	}

	var c configT
	err = json.Unmarshal(bytes, &c)
	if err != nil {
		return userDBT{}, map[string][]string{}, err
	}

	return c.UDB, c.GDB, nil
}

func main() {

	userDB, groupDB, err := getConfig()

	if err != nil {
		fmt.Fprintln(os.Stderr, "config error")
		os.Exit(-1)
	}

	if len(os.Args) == 1 {
		var userName, password string

		fmt.Scan(&userName, &password)

		user, userFound := userDB.findUser(userName)

		log.Printf("username is %v, userdata is %v, password is %v", userName, user, password)

		if userFound && user.Password == password {
			fmt.Printf("OK\n%s\n", user.Username)
			os.Exit(0)
		}

		fmt.Fprintln(os.Stderr, "Wrong Username or Password")
		fmt.Println("ERROR")
		os.Exit(-1)
	}

	if len(os.Args) == 2 || os.Args[1] != "-" {
		fmt.Fprintf(os.Stderr, "Incorrect argunments passed: %v\n", os.Args[1:])
		os.Exit(-1)
	}

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
