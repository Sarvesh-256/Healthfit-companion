from flask import Flask, render_template, request, jsonify, send_file, abort
from modules.bmi_tdee import calculate_bmi, bmi_category, calculate_bmr, calculate_tdee
from modules.fuzzy_mental_health import evaluate_mental_health
from modules.ann_fitness import predict_fitness
from modules.wellness_score import calculate_wellness_score
from modules.diet_recommendation import recommend_diet
from utils.data_storage import save_user_data

import os
import io
import json
import traceback
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/embed/index')
def embed_index():
    return render_template('embed_index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400

        payload = request.json
        form = payload.get('form') or payload

        # Read basic inputs (safe conversions)
        age = int(float(form.get('age', 0)))
        gender = str(form.get('gender', '')).lower()
        height = float(form.get('height', 0))
        weight = float(form.get('weight', 0))
        activity_level_str = str(form.get('activity_level', '')).lower()
        goal = str(form.get('goal', '')).lower()

        sleep = float(form.get('sleep', 0))
        stress = int(float(form.get('stress', 0)))
        mood = int(float(form.get('mood', 0)))
        screen = float(form.get('screen', 0))

        sedentary = float(form.get('sedentary', 0))
        recovery = float(form.get('recovery', 0))

        # Calculations
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level_str)

        mental_score, mental_status = evaluate_mental_health(sleep, stress, mood, screen)

        activity_map = {'sedentary': 1, 'light': 2, 'moderate': 3, 'active': 4, 'very_active': 5}
        activity_level_num = activity_map.get(activity_level_str, 3)

        fitness_level = predict_fitness(bmi, activity_level_num, sedentary, recovery)

        wellness_score, wellness_status = calculate_wellness_score(bmi, mental_score, fitness_level)

        # Diet recommendation
        diet_result = recommend_diet(tdee, goal)
        diet_rec = None
        if isinstance(diet_result, tuple):
            target_calories, foods_df = diet_result
            foods_records = []
            if hasattr(foods_df, 'to_dict'):
                try:
                    foods_records = foods_df.to_dict(orient='records')
                except Exception:
                    foods_records = []
            diet_rec = {'target_calories': int(round(target_calories)), 'goal': goal, 'foods': foods_records}
        elif hasattr(diet_result, 'to_dict'):
            try:
                foods_records = diet_result.to_dict(orient='records')
            except Exception:
                foods_records = []
            diet_rec = {'target_calories': None, 'goal': goal, 'foods': foods_records}
        elif isinstance(diet_result, dict):
            diet_rec = diet_result
        else:
            diet_rec = {'recommendation': str(diet_result), 'goal': goal}

        results = {
            'body_analysis': {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'bmi': round(bmi, 2),
                'bmi_category': category,
                'bmr': round(bmr, 2),
                'tdee': round(tdee, 2),
                'activity_level': activity_level_str,
            },
            'mental_health': {
                'sleep': sleep,
                'stress': stress,
                'mood': mood,
                'screen_time': screen,
                'mental_score': round(mental_score, 2),
                'mental_status': mental_status,
            },
            'fitness': {
                'sedentary_hours': sedentary,
                'recovery_hours': recovery,
                'fitness_level': fitness_level,
            },
            'wellness': {
                'wellness_score': wellness_score,
                'wellness_status': wellness_status,
            },
            'diet_recommendation': diet_rec,
        }

        return jsonify({'success': True, 'results': results})

    except Exception as e:
        print('ERROR in /api/calculate:', e)
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/save', methods=['POST'])
def save_assessment():
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400

        payload = request.json

        # Accept either computed results or raw form
        if 'results' in payload and isinstance(payload['results'], dict):
            results = payload['results']
            body = results.get('body_analysis', {})
            mental = results.get('mental_health', {})
            fitness = results.get('fitness', {})
            wellness = results.get('wellness', {})

            age = int(body.get('age') or 0)
            bmi = float(body.get('bmi') or 0)
            mental_score = float(mental.get('mental_score') or 0)
            fitness_level = str(fitness.get('fitness_level') or '')
            wellness_score = float(wellness.get('wellness_score') or 0)
            tdee = float(body.get('tdee') or 0)
            activity_level = str(body.get('activity_level') or '')

            weekly_sleep = float(mental.get('sleep') or 0) * 7
            weekly_stress = float(mental.get('stress') or 0) * 7
            weekly_mood = float(mental.get('mood') or 0) * 7
            weekly_screen = float(mental.get('screen_time') or mental.get('screen') or 0) * 7
            weekly_sedentary = float(fitness.get('sedentary_hours') or 0) * 7
            weekly_recovery = float(fitness.get('recovery_hours') or 0) * 7

        elif 'form' in payload and isinstance(payload['form'], dict):
            form = payload['form']
            age = int(float(form.get('age', 0)))
            gender = str(form.get('gender', '')).lower()
            height = float(form.get('height', 0))
            weight = float(form.get('weight', 0))
            activity_level = str(form.get('activity_level', '')).lower()

            sleep = float(form.get('sleep', 0))
            stress = int(float(form.get('stress', 0)))
            mood = int(float(form.get('mood', 0)))
            screen = float(form.get('screen', 0))

            sedentary = float(form.get('sedentary', 0))
            recovery = float(form.get('recovery', 0))

            bmi = calculate_bmi(weight, height)
            # reuse earlier helpers
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level)
            mental_score, _ = evaluate_mental_health(sleep, stress, mood, screen)
            activity_map = {'sedentary': 1, 'light': 2, 'moderate': 3, 'active': 4, 'very_active': 5}
            activity_level_num = activity_map.get(activity_level, 3)
            fitness_level = predict_fitness(bmi, activity_level_num, sedentary, recovery)
            wellness_score, _ = calculate_wellness_score(bmi, mental_score, fitness_level)

            weekly_sleep = sleep * 7
            weekly_stress = stress * 7
            weekly_mood = mood * 7
            weekly_screen = screen * 7
            weekly_sedentary = sedentary * 7
            weekly_recovery = recovery * 7

        else:
            return jsonify({'success': False, 'error': 'Request must include either "results" or "form" object'}), 400

        # Save via utils.data_storage.save_user_data
        save_user_data(age, bmi, mental_score, fitness_level, wellness_score, tdee,
                       activity_level, weekly_sleep, weekly_stress, weekly_mood,
                       weekly_screen, weekly_sedentary, weekly_recovery)

        saved_info = {
            'age': age,
            'bmi': bmi,
            'mental_score': mental_score,
            'fitness_level': fitness_level,
            'wellness_score': wellness_score,
            'tdee': tdee,
            'activity_level': activity_level,
            'weekly_sleep': weekly_sleep,
            'weekly_stress': weekly_stress,
            'weekly_mood': weekly_mood,
            'weekly_screen': weekly_screen,
            'weekly_sedentary': weekly_sedentary,
            'weekly_recovery': weekly_recovery,
        }

        # Append audit log
        try:
            log_entry = {'timestamp': datetime.utcnow().isoformat() + 'Z', 'payload': payload, 'saved': saved_info}
            os.makedirs('data', exist_ok=True)
            with open(os.path.join('data', 'save_log.jsonl'), 'a', encoding='utf-8') as lf:
                lf.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print('Failed to append save log:', e)

        return jsonify({'success': True, 'message': 'Assessment saved successfully', 'saved': saved_info})

    except Exception as e:
        print('ERROR in /api/save:', e)
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/report', methods=['POST'])
def generate_report():
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400

        payload = request.json
        results = payload.get('results') if isinstance(payload.get('results'), dict) else None
        if results is None:
            return jsonify({'success': False, 'error': 'Must send "results" object to generate PDF'}), 400

        buffer = io.BytesIO()
        # Try reportlab then fpdf fallback
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors

            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph('HealthFit Companion - Assessment Report', styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 12))

            # Body
            body = results.get('body_analysis', {})
            story.append(Paragraph('Body Analysis', styles['Heading2']))
            body_table_data = [['Metric', 'Value'], ['Age', body.get('age', '')], ['Height (cm)', body.get('height', '')],
                               ['Weight (kg)', body.get('weight', '')], ['BMI', body.get('bmi', '')],
                               ['BMI Category', body.get('bmi_category', '')], ['BMR (kcal)', body.get('bmr', '')],
                               ['TDEE (kcal)', body.get('tdee', '')]]
            t = Table(body_table_data, hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (1, 0), colors.lightgrey), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
            story.append(t)

            # Additional sections omitted for brevity (keeps behavior similar to previous implementation)
            doc.build(story)
            buffer.seek(0)
            return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='healthfit_report.pdf')

        except Exception:
            # Fallback to fpdf
            try:
                from fpdf import FPDF
            except Exception:
                return jsonify({'success': False, 'error': 'PDF generation requires reportlab or fpdf2'}), 500

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'HealthFit Companion - Assessment Report', ln=True, align='C')
            pdf.ln(6)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
            pdf.ln(6)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            buffer = io.BytesIO(pdf_output)
            buffer.seek(0)
            return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='healthfit_report.pdf')

    except Exception as e:
        print('ERROR in /api/report:', e)
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print('Starting HealthFit Companion Server...')
    app.run(debug=True, port=5000)
