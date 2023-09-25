console.log('hello world')
let delete_button = document.querySelector('#delete_button')

function confirm_delete()
{
    let ans = confirm("Are you sure you want to delete your account?");
}

function popUp()
{
    let popUpDiv = document.createElement("div");
    popUpDiv.id = "ready";
    popUpDiv.position = "relative"
    popUpDiv.style.width = "100px";
    popUpDiv.style.height = "100px";
    popUpDiv.style.color = "green";
    popUpDiv.style.zIndex = "-1";
    popUpDiv.innerText = "Ready to play?";
    document.getElementById("body").appendChild(popUpDiv);
}


function openForm()
{
    document.getElementById("popupForm").style.display = "block";
}
function closeForm()
{
    document.getElementById("popupForm").style.display = "none";
}
