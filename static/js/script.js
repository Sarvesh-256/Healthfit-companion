// ============================================
// HEALTHFIT COMPANION - FRONTEND LOGIC
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const healthForm = document.getElementById('healthForm');
    let latestResults = null;
    const resultsSection = document.getElementById('resultsSection');
    const assessmentForm = document.getElementById('assessmentForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    
    // Real-time slider value updates
    const stressSlider = document.getElementById('stress');
    const moodSlider = document.getElementById('mood');
    const stressValue = document.getElementById('stressValue');
    const moodValue = document.getElementById('moodValue');
    
    stressSlider.addEventListener('input', function() {
        stressValue.textContent = this.value;
    });
    
    moodSlider.addEventListener('input', function() {
        moodValue.textContent = this.value;
    });
    
    // Form submission
    healthForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Hide error message
        errorMessage.classList.add('hidden');
        
        // Collect form data
        const formData = {
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            height: document.getElementById('height').value,
            weight: document.getElementById('weight').value,
            activity_level: document.getElementById('activityLevel').value,
            goal: document.getElementById('goal').value,
            sleep: document.getElementById('sleep').value,
            stress: document.getElementById('stress').value,
            mood: document.getElementById('mood').value,
            screen: document.getElementById('screen').value,
            sedentary: document.getElementById('sedentary').value,
            recovery: document.getElementById('recovery').value
        };
        
        console.log('Submitting form data:', formData);
        
        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        assessmentForm.classList.add('hidden');
        resultsSection.classList.add('hidden');
        
        try {
            // Send data to backend
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            console.log('Response status:', response.status, response.statusText);
            
            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.success) {
                displayResults(data.results);
                resultsSection.classList.remove('hidden');
                loadingSpinner.classList.add('hidden');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                showError(data.error || 'An error occurred during assessment');
                assessmentForm.classList.remove('hidden');
                loadingSpinner.classList.add('hidden');
            }
        } catch(error) {
            console.error('Fetch error:', error);
            showError('Error connecting to server: ' + error.message);
            assessmentForm.classList.remove('hidden');
            loadingSpinner.classList.add('hidden');
        }
    });
    
    // Display results
    function displayResults(results) {
        // store latest results for save/report actions
        latestResults = results;
        const body = results.body_analysis;
        const mental = results.mental_health;
        const fitness = results.fitness;
        const wellness = results.wellness;
        const diet = results.diet_recommendation;
        
        // Body Analysis
        document.getElementById('resultBMI').textContent = body.bmi;
        document.getElementById('resultBMICategory').textContent = body.bmi_category;
        document.getElementById('resultBMR').textContent = Math.round(body.bmr);
        document.getElementById('resultTDEE').textContent = Math.round(body.tdee);
        document.getElementById('resultBodyInfo').textContent = 
            `Your daily caloric need is approximately ${Math.round(body.tdee)} calories`;
        
        // Mental Health
        document.getElementById('resultMentalScore').textContent = mental.mental_score;
        document.getElementById('resultMentalStatus').textContent = mental.mental_status;
        document.getElementById('resultSleep').textContent = mental.sleep;
        document.getElementById('resultStress').textContent = mental.stress;
        document.getElementById('resultScreen').textContent = mental.screen_time;
        
        // Fitness
        document.getElementById('resultFitnessLevel').textContent = fitness.fitness_level;
        document.getElementById('resultSedentary').textContent = fitness.sedentary_hours;
        document.getElementById('resultRecovery').textContent = fitness.recovery_hours;
        
        // Wellness Score
        const wellnessScore = wellness.wellness_score;
        document.getElementById('resultWellnessScore').textContent = wellnessScore;
        const wellnessFill = document.getElementById('wellnessFill');
        wellnessFill.style.width = (wellnessScore * 10) + '%';
        
        // Diet Recommendation
        const dietElement = document.getElementById('dietRecommendation');
        if (typeof diet === 'string') {
            dietElement.innerHTML = diet;
        } else if (typeof diet === 'object' && diet !== null) {
            dietElement.innerHTML = formatDietRecommendation(diet);
        } else {
            dietElement.textContent = 'No specific recommendation available';
        }
    }
    
    // Format diet recommendation
    function formatDietRecommendation(diet) {
        // If backend sent a simple recommendation string
        if (diet.recommendation && typeof diet.recommendation === 'string') {
            return `<p>${diet.recommendation}</p>`;
        }

        // If backend returned a structured diet plan
        if (diet.target_calories && Array.isArray(diet.foods)) {
            let html = `<p><strong>Target Daily Calories:</strong> ${diet.target_calories} &nbsp; <strong>Goal:</strong> ${formatLabel(diet.goal)}</p>`;
            html += '<div class="food-table-container"><table class="food-table"><thead><tr><th>Food</th><th>Calories</th><th>Protein</th><th>Carbs</th><th>Fat</th></tr></thead><tbody>';

            diet.foods.forEach(item => {
                const food = item.Food || item.food || item.name || '';
                const cals = item.Calories ?? item.calories ?? '';
                const protein = item.Protein ?? item.protein ?? '';
                const carbs = item.Carbs ?? item.carbs ?? '';
                const fat = item.Fat ?? item.fat ?? '';
                html += `<tr><td>${food}</td><td>${cals}</td><td>${protein}</td><td>${carbs}</td><td>${fat}</td></tr>`;
            });

            html += '</tbody></table></div>';
            return html;
        }

        // Fallback: render generic object
        let html = '<ul>';
        for (const [key, value] of Object.entries(diet)) {
            html += `<li><strong>${formatLabel(key)}:</strong> ${value}</li>`;
        }
        html += '</ul>';
        return html;
    }
    
    // Format label
    function formatLabel(str) {
        return str
            .replace(/_/g, ' ')
            .replace(/\b\w/g, char => char.toUpperCase());
    }
    
    // New Assessment Button
    document.getElementById('newAssessmentBtn').addEventListener('click', function() {
        healthForm.reset();
        resultsSection.classList.add('hidden');
        assessmentForm.classList.remove('hidden');
        errorMessage.classList.add('hidden');
        stressValue.textContent = '5';
        moodValue.textContent = '5';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // Save Assessment
    document.getElementById('saveAssessmentBtn').addEventListener('click', async function() {
        // Prefer sending the latest computed results; fall back to form values
        const payload = {
            timestamp: new Date().toISOString()
        };

        if (latestResults) {
            payload.results = latestResults;
        } else {
            payload.form = {
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                height: document.getElementById('height').value,
                weight: document.getElementById('weight').value,
                activity_level: document.getElementById('activityLevel').value,
                goal: document.getElementById('goal') ? document.getElementById('goal').value : null,
                sleep: document.getElementById('sleep').value,
                stress: document.getElementById('stress').value,
                mood: document.getElementById('mood').value,
                screen: document.getElementById('screen').value,
                sedentary: document.getElementById('sedentary').value,
                recovery: document.getElementById('recovery').value
            };
        }

        try {
            const response = await fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            console.log('Save payload:', payload);
            console.log('Save response:', data);
            if (data.success) {
                alert('Assessment saved successfully! (Check VS Code terminal for details)');
            } else {
                showError(data.error || 'Failed to save assessment');
            }
        } catch (error) {
            showError('Error saving assessment: ' + error.message);
        }
    });
    
    // Download Report (PDF)
    document.getElementById('downloadReportBtn').addEventListener('click', async function() {
        // Use latestResults if available
        const payload = { timestamp: new Date().toISOString() };
        if (latestResults) payload.results = latestResults;
        else {
            // Build results from DOM as fallback
            payload.results = {
                body_analysis: {
                    bmi: document.getElementById('resultBMI').textContent,
                    bmi_category: document.getElementById('resultBMICategory').textContent,
                    bmr: document.getElementById('resultBMR').textContent,
                    tdee: document.getElementById('resultTDEE').textContent
                },
                mental_health: {
                    mental_score: document.getElementById('resultMentalScore').textContent,
                    mental_status: document.getElementById('resultMentalStatus').textContent,
                    sleep: document.getElementById('resultSleep').textContent,
                    stress: document.getElementById('resultStress').textContent
                },
                fitness: {
                    fitness_level: document.getElementById('resultFitnessLevel').textContent,
                    sedentary_hours: document.getElementById('resultSedentary').textContent,
                    recovery_hours: document.getElementById('resultRecovery').textContent
                },
                wellness: {
                    wellness_score: document.getElementById('resultWellnessScore').textContent
                }
            };
        }
        // Generate PDF client-side using jsPDF
        try {
            const results = payload.results;
            generatePdfWithJsPDF(results);
        } catch (err) {
            console.error('Client PDF generation error:', err);
            showError('Failed to generate PDF in browser: ' + err.message);
        }
    });

    // Client-side PDF generator using jsPDF
    function generatePdfWithJsPDF(results) {
        if (!window.jspdf || !window.jspdf.jsPDF) {
            throw new Error('jsPDF not loaded');
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({ unit: 'pt', format: 'letter' });
        const margin = 40;
        let y = 40;

        doc.setFontSize(18);
        doc.text('HealthFit Companion - Assessment Report', doc.internal.pageSize.getWidth() / 2, y, { align: 'center' });
        y += 24;
        doc.setFontSize(10);
        doc.text(`Generated: ${new Date().toLocaleString()}`, margin, y);
        y += 18;

        function addSectionTitle(title) {
            doc.setFontSize(12);
            doc.setFont(undefined, 'bold');
            doc.text(title, margin, y);
            y += 14;
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
        }

        function addKV(key, val) {
            const keyX = margin;
            const valX = margin + 200;
            doc.text(`${key}:`, keyX, y);
            doc.text(String(val ?? ''), valX, y);
            y += 12;
            if (y > doc.internal.pageSize.getHeight() - 60) {
                doc.addPage();
                y = margin;
            }
        }

        // Body Analysis
        addSectionTitle('Body Analysis');
        const body = results.body_analysis || {};
        addKV('BMI', body.bmi);
        addKV('BMI Category', body.bmi_category);
        addKV('BMR (kcal)', body.bmr);
        addKV('TDEE (kcal)', body.tdee);
        y += 6;

        // Mental Health
        addSectionTitle('Mental Health');
        const mental = results.mental_health || {};
        addKV('Mental Score', mental.mental_score);
        addKV('Status', mental.mental_status);
        addKV('Sleep (hrs/day)', mental.sleep);
        addKV('Stress (0-10)', mental.stress);
        addKV('Screen time (hrs/day)', mental.screen_time || mental.screen);
        y += 6;

        // Fitness & Wellness
        addSectionTitle('Fitness & Wellness');
        const fitness = results.fitness || {};
        const wellness = results.wellness || {};
        addKV('Fitness Level', fitness.fitness_level);
        addKV('Sedentary (hrs/day)', fitness.sedentary_hours);
        addKV('Recovery (hrs/day)', fitness.recovery_hours);
        addKV('Wellness Score', wellness.wellness_score);
        y += 6;

        // Diet Recommendation
        const diet = results.diet_recommendation || {};
        if (diet && (diet.foods || diet.target_calories)) {
            addSectionTitle('Diet Recommendation');
            addKV('Target Calories', diet.target_calories ?? '');
            y += 6;

            // If autoTable plugin available, build a table
            if (doc.autoTable && Array.isArray(diet.foods) && diet.foods.length) {
                const head = [['Food', 'Calories', 'Protein', 'Carbs', 'Fat']];
                const bodyRows = diet.foods.map(f => [f.Food || f.food || f.name || '', f.Calories ?? f.calories ?? '', f.Protein ?? f.protein ?? '', f.Carbs ?? f.carbs ?? '', f.Fat ?? f.fat ?? '']);
                doc.autoTable({ startY: y, head: head, body: bodyRows, margin: { left: margin, right: margin } });
                y = doc.lastAutoTable ? doc.lastAutoTable.finalY + 10 : y + (diet.foods.length * 12) + 10;
            } else if (Array.isArray(diet.foods) && diet.foods.length) {
                // Simple fallback rendering
                doc.setFontSize(10);
                doc.setFont(undefined, 'bold');
                doc.text('Food', margin, y);
                doc.text('Calories', margin + 220, y);
                y += 12;
                doc.setFont(undefined, 'normal');
                diet.foods.forEach(item => {
                    doc.text(item.Food || item.food || item.name || '', margin, y);
                    doc.text(String(item.Calories ?? item.calories ?? ''), margin + 220, y);
                    y += 12;
                    if (y > doc.internal.pageSize.getHeight() - 60) {
                        doc.addPage();
                        y = margin;
                    }
                });
            }
        }

        // Save PDF
        const filename = 'healthfit_report_' + Date.now() + '.pdf';
        doc.save(filename);
    }
    
    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }
    
    // Download file helper
    function downloadFile(content, filename) {
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
});
