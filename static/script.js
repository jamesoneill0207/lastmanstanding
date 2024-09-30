document.addEventListener("DOMContentLoaded", function() {
    const currentDate = new Date(); 
    const gameweek = document.getElementById("gameweek");
    
    Array.from(gameweek.options).forEach(option => {
        const deadline = new Date(option.getAttribute("data-deadline"));
        if (deadline <= currentDate) {
            option.remove(); 
        }
    });
});

