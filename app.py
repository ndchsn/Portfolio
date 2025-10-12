from flask import Flask, render_template, url_for

from flask import Flask, render_template, url_for

from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


@app.route('/')
def index():
    # determine which profile photo to use (prefer user-supplied PNG)
    static_images = os.path.join(app.static_folder, 'images')
    if os.path.exists(os.path.join(static_images, 'photo.png')):
        photo = url_for('static', filename='images/photo.png')
    elif os.path.exists(os.path.join(static_images, 'photo2.svg')):
        photo = url_for('static', filename='images/photo2.svg')
    else:
        photo = url_for('static', filename='images/photo.svg')

    profile = {
        'name': 'Andi Muhammad Ichsan Jalaluddin',
        'headline': 'Cloud Engineer | DevOps Engineer',
        'summary': 'Cloud-focused DevOps engineer with experience designing, automating, and operating scalable cloud-native systems. Passionate about infrastructure as code, CI/CD, containers, and observability.',
        'photo_url': photo,
        'contact': {
            'email': 'andiichsan123@gmail.com',
            'phone': '+62 812 3456 7890',
            'location': 'Jakarta, Indonesia'
        },
        'experiences': [
            {
                'role': 'Cloud Engineer',
                'company': 'Multipolar Technology',
                'period': '2023 - Present',
                'details': 'Built CI/CD pipelines, migrated monoliths to Kubernetes, and automated infra with Terraform.'
            },
            {
                'role': 'Cloud Computing Cohort',
                'company': 'Bangkit Academy (GoTo) - Google, Gojek, Traveloka',
                'period': '2023 - 2024',
                'details': 'Managed multi-cloud deployments and implemented monitoring and cost-optimization.'
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Computer Engineering',
                'school': 'Universitas Amikom Yogyakarta',
                'year': '2020 - 2024'
            }
        ],
        'certificates': [
            'GCP Professional Cloud Architect',
            'GCP Professional Cloud Network Engineer',
            'GCP Professional Cloud Security Engineer',
            'GCP Professional Cloud Developer',
            'GCP Professional Cloud DevOps Engineer',
            'Azure az-500 Security Engineer',
            'Azure az-104 Administrator'
        ],
        'skills': [
            'Google Cloud Platform', 'Microsoft Azure', 'Terraform', 'Docker', 'CI/CD (GitHub Actions, GitLab CI)', 'Prometheus & Grafana', 'Linux', 'Python', 'Kubernetes'
        ]
    }
    return render_template('index.html', profile=profile)


if __name__ == '__main__':
    app.run(debug=True)
