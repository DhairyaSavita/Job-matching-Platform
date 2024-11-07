document.getElementById('add-job').onclick = async function () {
    const title = document.getElementById('job-title').value;
    const skills = document.getElementById('job-skills').value;

    const response = await fetch('/add-job', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, skills: skills }),
    });

    if (response.ok) {
        alert('Job added!');
    }
};
document.getElementById('match-jobs').onclick = async function () {
    const userId = document.getElementById('user-id').value;
    const response = await fetch(`/match-jobs/${userId}`);

    if (response.ok) {
        const matchedJobs = await response.json();
        const jobsDiv = document.getElementById('matched-jobs');
        jobsDiv.innerHTML = '<h3>Matched Jobs:</h3>';
        matchedJobs.forEach(job => {
            jobsDiv.innerHTML += `<p>${job.title} - Skills: ${job.skills.join(', ')}</p>`;
        });
    }
};
