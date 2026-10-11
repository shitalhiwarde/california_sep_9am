const form = document.getElementById("prediction-form");
const button = document.getElementById("predict-button");
const result = document.getElementById("result");
const price = document.getElementById("price");
const message = document.getElementById("message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    message.textContent = "";
    result.hidden = true;
    button.disabled = true;
    button.textContent = "Predicting...";

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    for (const key in data) {
        data[key] = Number(data[key]);
    }

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const output = await response.json();

        if (!response.ok || !output.success) {
            throw new Error(output.error || "Prediction failed.");
        }

        price.textContent = output.formatted_price;
        result.hidden = false;

    } catch (error) {
        message.textContent = error.message;
    } finally {
        button.disabled = false;
        button.textContent = "Predict House Price";
    }
});