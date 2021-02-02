async function fetchFilterData(event) {
    event.preventDefault();
    const bMapDiv = document.getElementById("bubbleMap");
    bMapDiv.innerHTML = '<div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading Reddit Heat Data...</span></div>';

    const data_date = document.getElementById("startDatePicker").value;
    const heat_limit = document.getElementById("minRedditHeat").value;
    try {
        let res = await axios.get(`/api/date/${data_date}?heat=${heat_limit}`);
        if (res.data.error) {
            bMapDiv.innerHTML = res.data.error;
        }
        else {
            buildBubbleChart(res.data);
        }
    }
    catch (err) {
        bMapDiv.innerHTML = "Unable to fetch data!";
    }
}

//////////////////////////
// Event Listeners
//////////////////////////
document.addEventListener("DOMContentLoaded", fetchFilterData); // Perform first data fetch after page loads
document.getElementById("submitFilterForm").addEventListener("click", fetchFilterData);