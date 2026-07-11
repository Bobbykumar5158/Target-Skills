function toggleDetails(modalId, shouldOpen) {
    // Look up the unique modal element by its clean ID string
    const overlayTarget = document.getElementById(modalId);
    console.log(modalId)
    console.log(overlayTarget)

    if (overlayTarget) {
        if (shouldOpen) {
            overlayTarget.style.display = "flex";
        } else if (!shouldOpen) {
            overlayTarget.style.display = "none";
        }
    }
}

function showLoader() {
    document.getElementById("loadingOverlay").style.display = "flex";

    const emptyState = document.querySelector(".empty-state-container");
    const resultsState = document.querySelector(".results-container");

    if (emptyState) emptyState.style.display = "none";
    if (resultsState) resultsState.style.display = "none";
}