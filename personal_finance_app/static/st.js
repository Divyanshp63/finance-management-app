// Example: Add expense dynamically
function addExpense() {
    const category = document.getElementById("category").value;
    const amount = document.getElementById("amount").value;

    if (category && amount) {
        const ul = document.getElementById("expense-list");
        const li = document.createElement("li");
        li.textContent = `${category} - ₹${amount}`;

        // delete button
        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = () => ul.removeChild(li);

        li.appendChild(btn);
        ul.appendChild(li);

        // clear inputs
        document.getElementById("category").value = "";
        document.getElementById("amount").value = "";
    } else {
        alert("Please enter category and amount!");
    }
}