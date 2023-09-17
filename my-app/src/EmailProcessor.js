import React, { useState, useEffect } from 'react';

function EmailProcessor(props) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/process_emails')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setData(data); // Directly setting the received data
                setLoading(false);
                
                // Calculate the counts of 'relevant' and 'irrelevant'
                const relevantCount = data.categorized_results.filter(item => item === 'relevant').length;
                const irrelevantCount = data.categorized_results.filter(item => item === 'irrelevant').length;

                // Update the parent component with these counts
                props.updateCounts(relevantCount, irrelevantCount);

            })
            .catch(error => {
                setError(error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    const filteredResults = data.categorized_results.filter(item => ['irrelevant', 'relevant'].includes(item));

    return (
        <div>
            {/* Render your filtered data here */}
            <pre>{JSON.stringify(filteredResults, null)}</pre>
        </div>
    );
}

export default EmailProcessor;