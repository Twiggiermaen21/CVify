import sys

with open('web/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """                <!-- 5. Projekty -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Wybrane Projekty</h2>
                        <button class="btn-outline btn-small" onclick="addProject()">+ Dodaj projekt</button>
                    </div>
                    <div id="projects-container"></div>
                </div>

                <!-- 6. Umiejętności -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Umiejętności i Technologie</h2>
                    </div>
                    <div class="form-group">
                        <label>Frontend (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-frontend" class="form-control" oninput="updateSkillsCat('Frontend', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Backend & AI (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-backend" class="form-control" oninput="updateSkillsCat('Backend', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Bazy danych (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-db" class="form-control" oninput="updateSkillsCat('Bazy danych', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Narzędzia & DevOps (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-devops" class="form-control" oninput="updateSkillsCat('Narzędzia & DevOps', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Umiejętności miękkie (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-soft" class="form-control" oninput="updateSoftSkills(this.value)">
                    </div>
                </div>

                <!-- 7. Wykształcenie -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Wykształcenie</h2>
                        <button class="btn-outline btn-small" onclick="addEducation()">+ Dodaj edukację</button>
                    </div>
                    <div id="education-container"></div>
                </div>

                <!-- 8. Języki -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Języki obce</h2>
                        <button class="btn-outline btn-small" onclick="addLanguage()">+ Dodaj język</button>
                    </div>
                    <div id="languages-container"></div>
                </div>"""

replacement = """                <!-- 5. Wykształcenie -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Wykształcenie</h2>
                        <button class="btn-outline btn-small" onclick="addEducation()">+ Dodaj edukację</button>
                    </div>
                    <div id="education-container"></div>
                </div>

                <!-- 6. Języki obce -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Języki obce</h2>
                        <button class="btn-outline btn-small" onclick="addLanguage()">+ Dodaj język</button>
                    </div>
                    <div id="languages-container"></div>
                </div>

                <!-- 7. Umiejętności i Technologie (pod językami obcymi) -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Umiejętności i Technologie</h2>
                    </div>
                    <div class="form-group">
                        <label>Frontend (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-frontend" class="form-control" oninput="updateSkillsCat('Frontend', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Backend & AI (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-backend" class="form-control" oninput="updateSkillsCat('Backend', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Bazy danych (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-db" class="form-control" oninput="updateSkillsCat('Bazy danych', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Narzędzia & DevOps (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-devops" class="form-control" oninput="updateSkillsCat('Narzędzia & DevOps', this.value)">
                    </div>
                    <div class="form-group" style="display:none;">
                        <label>Umiejętności miękkie (oddzielaj przecinkami)</label>
                        <input type="text" id="sk-soft" class="form-control" oninput="updateSoftSkills(this.value)">
                    </div>
                </div>

                <!-- 8. Wybrane Projekty -->
                <div class="form-section">
                    <div class="section-header">
                        <h2>Wybrane Projekty</h2>
                        <button class="btn-outline btn-small" onclick="addProject()">+ Dodaj projekt</button>
                    </div>
                    <div id="projects-container"></div>
                </div>"""

norm_target = target.replace("\r\n", "\n")
norm_content = content.replace("\r\n", "\n")
norm_replacement = replacement.replace("\r\n", "\n")

if norm_target in norm_content:
    new_content = norm_content.replace(norm_target, norm_replacement)
    with open('web/templates/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: index.html updated")
else:
    print("ERROR: norm_target not in norm_content")
