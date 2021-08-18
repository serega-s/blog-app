const csrf = document.getElementById("csrf").value
console.log("CSRF, " + csrf)

const btnSubmit = document.getElementById("btnSubmit")

function login() {
  const username = document.getElementById("loginUsername").value
  const password = document.getElementById("loginPassword").value

  if (!username && !password) {
    alert("You must enter both!")
  }

  const data = {
    username: username,
    password: password,
  }

  fetch("/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify(data),
  })
    .then((result) => result.json())
    .then((response) => {
      console.log(response)
      response.status == 200
        ? (window.location.href = "/")
        : alert(response.message)
    })
}

function register() {
  const username = document.getElementById("loginUsername").value
  const password = document.getElementById("loginPassword").value

  if (!username && !password) {
    alert("You must enter both!")
  }

  const data = {
    username: username,
    password: password,
  }

  fetch("/api/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify(data),
  })
    .then((result) => result.json())
    .then((response) => {
      console.log(response)
      response.status == 200
        ? (window.location.href = "/")
        : alert(response.message)
    })
}
