$(document).ready(function() {
    $('#applicationsTable').DataTable({
        "paging": true,       // Enable pagination
        "searching": true,    // Enable searching
        "info": true,         // Show table information
        "ordering": true,     // Enable sorting
        "responsive": true,   // Make table responsive
        "lengthMenu": [10, 25, 50, 75, 100], // Options for number of rows per page
    });
});
