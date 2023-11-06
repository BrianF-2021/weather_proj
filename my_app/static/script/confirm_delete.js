// document.getElementById('btn_delete').addEventListener('click', function() {
//     var confirmDelete = confirm("Are you sure you want to delete your account?");
    
//     if (confirmDelete) {
//         // Code to delete account goes here
//         alert("Account deleted!");
//     } else {
//         alert("Account not deleted.");
//     }
// });

let data_box = document.getElementById('delete_account');

document.getElementById('btn_delete').addEventListener('click', function() {
	confirmDelete();
});



function confirmDelete() {
	let popup = document.createElement("div");
	popup.classList.add("popup");
	popup.innerHTML = `
	<h1>DELETE YOUR ACCOUNT?</h1>
	<div>
		<a id="btn_cancel" onclick="cancelDelete()">Cancel</a>
		<a id="delete_user" onclick="cancelDelete()" href="/user/delete">Delete Account</a>
	</div>
`;
	data_box.appendChild(popup);
}

function cancelDelete() {
	var popup = document.querySelector(".popup");
	data_box.removeChild(popup);
}






