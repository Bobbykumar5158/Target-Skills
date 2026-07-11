function switchWorkspaceView(targetId, elementRef) {
        const operationalViews = document.querySelectorAll('.track-main-workspace');
        operationalViews.forEach(view => view.style.display = 'none');

        const pillButtons = document.querySelectorAll('.pill-toggle-btn');
        pillButtons.forEach(btn => btn.classList.remove('active'));

        document.getElementById(targetId).style.display = 'block';
        elementRef.classList.add('active');
    }