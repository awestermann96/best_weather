document.getElementById("demo").innerHTML = "Hello JavaScript";

<button type="button" onclick="document.getElementById('demo').style.fontSize='35px'">Click Me!</button>

// one statemenet many variables
let person = "John Doe", carName = "Volvo", price = 200;

function myFunction(a, b) {
    // Function returns the product of a and b
      return a * b;
    }

// objects - object literal
const car = {type:"Fiat", model:"500", color:"white"};

// Create an Object
const person = new Object();

// Add Properties
person.firstName = "John";
person.lastName = "Doe";
person.age = 50;
person.eyeColor = "blue";

const person = {
    firstName: "John",
    lastName : "Doe",
    id       : 5566,
    fullName : function() {
      return this.firstName + " " + this.lastName;
    }
  };
  
  function Person(first, last, age, eyecolor) {
    this.firstName = first;
    this.lastName = last;
    this.age = age;
    this.eyeColor = eyecolor;
    this.nationality = "English";
  }

  let text = `Welcome ${firstName}, ${lastName}!`;

  // arrays
  for (let i = 0; i < fLen; i++) {
    text += "<li>" + fruits[i] + "</li>";
  }

let text2 = "<ul>";
fruits.forEach(myFunction);
text2 += "</ul>";

function myFunction(value) {
  text += "<li>" + value + "</li>";
}

for (let i in myObj.cars) {
    x += "<h1>" + myObj.cars[i].name + "</h1>";
    for (let j in myObj.cars[i].models) {
      x += myObj.cars[i].models[j];
    }
  }

// conditionals 
if (age < 18) text = "Too young to buy alcohol";
let voteable = (age < 18) ? "Too young":"Old enough";

if (time < 10) {
  greeting = "Good morning";
} else if (time < 20) {
  greeting = "Good day";
} else {
  greeting = "Good evening";
}

switch (new Date().getDay()) {
  case 4:
  case 5:
    text = "Soon it is Weekend";
    break; 
  case 0: // 0 and 6 same block
  case 6:
    text = "It is Weekend";
    break;
  default: 
    text = "Looking forward to the Weekend";
}