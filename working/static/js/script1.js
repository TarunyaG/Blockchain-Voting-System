// /static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    const voteBoxes = document.querySelectorAll('.vote-box');

    voteBoxes.forEach(box => {
        box.addEventListener('click', function (e) {
            // Prevent multiple selection
            voteBoxes.forEach(b => b.classList.remove('selected'));

            // Add 'selected' to the current box
            this.classList.add('selected');

            // Check the radio input inside this label
            const radioInput = this.querySelector('input[type=radio]');
            if (radioInput) {
                radioInput.checked = true;
                console.log('Selected candidate:', radioInput.value);  // Debugging
            }
        });
    });

    // Handle form submission
    document.querySelector('form').addEventListener('submit', function (e) {
        const selectedVote = document.querySelector('input[type=radio]:checked');
        if (!selectedVote) {
            alert('Please select a candidate before confirming.');
            e.preventDefault();  // Stop form submission
        } else {
            alert('Vote confirmed for ' + selectedVote.value);
        }
    });
});
