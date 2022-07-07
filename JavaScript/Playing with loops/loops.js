for (let i = 0; i<=9; i++) {
    console.log(i)
}

const users = ["Samson", "Anna", "Joel"];

for (const user of users) {
    console.log(user);
}

const loggedInUser = {
    name: "Samson",
    age: 22,
    isAdmin : true
}

for (const propertyName in loggedInUser) {
    console.log(propertyName);
    //console.log(loggedInUser[propertyName]);
} 

let isFinished = false;

while (!isFinished) {
    isFinished = confirm("Do you want to quit?")
}