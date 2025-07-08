function setupSectionRandomSelects() {
  document.querySelectorAll(".section-fieldset").forEach((fieldset) => {
    ["instruments", "drums", "effects"].forEach((group) => {
      const groupDiv = fieldset.querySelector(
        `.checkbox-group[data-group='${group}']`
      );
      if (!groupDiv) return;
      const randomBox = groupDiv.querySelector(".random-checkbox");
      const optionBoxes = groupDiv.querySelectorAll(".option-checkbox");

      randomBox.addEventListener("change", () => {
        if (randomBox.checked) {
          optionBoxes.forEach((box) => {
            box.checked = false;
          });
        }
      });

      optionBoxes.forEach((box) => {
        box.addEventListener("change", () => {
          if (box.checked) randomBox.checked = false;
        });
      });
    });
  });
}

function createSectionControls(idx, section = {}) {
  const instruments = [
    "guitar",
    "piano",
    "violin",
    "synth_lead",
    "synth_pad",
    "organ",
    "bell",
    "flute",
    "clarinet",
    "cello",
    "trumpet",
    "trombone",
    "french_horn",
    "oboe",
    "saxophone",
    "synth_bass",
    "marimba",
    "choir",
    "bass",
  ];
  const drums = ["kick", "snare", "hihat"];
  const effects = [
    "delay",
    "chorus",
    "flanger",
    "phaser",
    "reverb",
    "granular",
    "eq",
    "compressor",
    "limiter",
    "stereo",
    "spatial",
  ];
  const removeBtn =
    idx === 0
      ? ""
      : `<button type="button" class="remove-section-btn" data-section="${idx}">Remove</button>`;

  function renderCheckboxGroup(groupName, options, selected) {
    const sel = selected && selected.length > 0 ? selected : ["__random__"];
    let html = `<div class="checkbox-group" data-group="${groupName}">`;
    html += `<label><input type="checkbox" name="section_${groupName}_${idx}" value="__random__" class="random-checkbox"${
      sel.includes("__random__") ? " checked" : ""
    }> Random</label>`;
    options.forEach((opt) => {
      html += `<label><input type="checkbox" name="section_${groupName}_${idx}" value="${opt}" class="option-checkbox"${
        sel.includes(opt) ? " checked" : ""
      }> ${opt}</label>`;
    });
    html += `</div>`;
    return html;
  }
  return `
    <fieldset class="section-fieldset" data-section="${idx}">
        <legend>Section ${idx + 1} ${removeBtn}</legend>
        <div class="section-row">
            <label>Duration (s): <input type="number" name="section_duration_${idx}" min="4" value="${
    section.duration || 4
  }"></label>
            <label>Tempo (BPM): <input type="number" name="section_tempo_${idx}" min="40" max="240" value="${
    section.tempo || 120
  }"></label>
            <label>Key:
                <select name="section_key_${idx}">
                    ${["C", "D", "E", "F", "G", "A", "B"]
                      .map(
                        (k) =>
                          `<option value="${k}"${
                            section.key === k ? " selected" : ""
                          }>${k}</option>`
                      )
                      .join("")}
                </select>
            </label>
            <label>Scale:
                <select name="section_scale_${idx}">
                    ${["major", "minor", "pentatonic", "blues"]
                      .map(
                        (s) =>
                          `<option value="${s}"${
                            section.scale === s ? " selected" : ""
                          }>${s}</option>`
                      )
                      .join("")}
                </select>
            </label>
        </div>
        <label>Instruments:
            ${renderCheckboxGroup(
              "instruments",
              instruments,
              section.instruments
            )}
        </label>
        <label>Drums:
            ${renderCheckboxGroup("drums", drums, section.drums)}
        </label>
        <label>Effects:
            ${renderCheckboxGroup("effects", effects, section.effects)}
        </label>
    </fieldset>
    `;
}

function renderSections(sections) {
  const container = document.getElementById("sections-container");
  container.innerHTML = sections
    .map((s, i) => createSectionControls(i, s))
    .join("");

  document.querySelectorAll(".remove-section-btn").forEach((btn) => {
    btn.onclick = function () {
      sections.splice(parseInt(btn.dataset.section), 1);
      renderSections(sections);
    };
  });
  setupSectionRandomSelects();

  document
    .querySelectorAll('.section-fieldset input[type="checkbox"]')
    .forEach((cb) => {
      cb.addEventListener("change", function () {
        setTimeout(updateConfigPreview, 0);
      });
    });

  document
    .querySelectorAll(
      '.section-fieldset input[type="number"], .section-fieldset select'
    )
    .forEach((el) => {
      el.addEventListener("change", function () {
        setTimeout(updateConfigPreview, 0);
      });
      el.addEventListener("input", function () {
        setTimeout(updateConfigPreview, 0);
      });
    });

  setTimeout(updateConfigPreview, 0);
}

function getSectionsFromForm() {
  const fieldsets = document.querySelectorAll(".section-fieldset");
  const sections = [];
  fieldsets.forEach((fs, idx) => {
    const name = `Section ${idx + 1}`;
    const duration =
      parseInt(fs.querySelector(`[name='section_duration_${idx}']`).value) || 4;
    const tempo =
      parseInt(fs.querySelector(`[name='section_tempo_${idx}']`).value) || 120;
    const key = fs.querySelector(`[name='section_key_${idx}']`).value;
    const scale = fs.querySelector(`[name='section_scale_${idx}']`).value;

    function getChecked(group) {
      return Array.from(
        fs.querySelectorAll(
          `.checkbox-group[data-group='${group}'] input[type='checkbox']:checked`
        )
      ).map((cb) => cb.value);
    }
    const instruments = getChecked("instruments");
    const drums = getChecked("drums");
    const effects = getChecked("effects");
    sections.push({
      name,
      duration,
      tempo,
      key,
      scale,
      instruments,
      drums,
      effects,
    });
  });
  return sections;
}

function updateConfigPreview() {
  const sameForAll = document.getElementById("same-for-all");
  const configPreview = document.getElementById("config-preview");
  let sectionData =
    sameForAll && sameForAll.checked
      ? [getSectionsFromForm()[0]]
      : getSectionsFromForm();

  let structure = window.structure || [];

  const names = sectionData.map((s) => s.name);
  structure = structure.filter((n) => names.includes(n));
  if (structure.length === 0 && names.length > 0) structure = [names[0]];

  window.structure = structure;
  const config = { structure, sections: sectionData };
  if (configPreview)
    configPreview.textContent = JSON.stringify(config, null, 2);
}

document.addEventListener("DOMContentLoaded", () => {
  const sameForAll = document.getElementById("same-for-all");
  const addSectionBtn = document.getElementById("add-section-btn");
  const structureList = document.getElementById("structure-list");
  const addToStructureBtn = document.getElementById("add-to-structure-btn");
  const configPreview = document.getElementById("config-preview");
  const configPreviewToggle = document.getElementById("config-preview-toggle");
  const configPreviewWrapper = document.getElementById(
    "config-preview-wrapper"
  );
  const downloadConfigBtn = document.getElementById("download-config-btn");
  let sections = [
    {
      name: "Section 1",
      duration: 4,
      instruments: ["__random__"],
      drums: ["__random__"],
      effects: ["__random__"],
    },
  ];
  let structure = [sections[0].name];

  function setConfigPreviewCollapsed(collapsed) {
    if (collapsed) {
      configPreviewWrapper.classList.add("collapsed");
      configPreviewToggle.innerHTML =
        '<span class="arrow">&#9654;</span> Config Preview';
      downloadConfigBtn.style.display = "none";
    } else {
      configPreviewWrapper.classList.remove("collapsed");
      configPreviewToggle.innerHTML =
        '<span class="arrow">&#9660;</span> Config Preview';
      downloadConfigBtn.style.display = "";
    }
  }
  configPreviewToggle.addEventListener("click", () => {
    const collapsed = !configPreviewWrapper.classList.contains("collapsed");
    setConfigPreviewCollapsed(collapsed);
  });

  setConfigPreviewCollapsed(true);

  function updateSectionUI() {
    if (sameForAll.checked) {
      addSectionBtn.style.display = "none";
      renderSections([sections[0]]);
    } else {
      addSectionBtn.style.display = "";
      renderSections(sections);
    }

    const names = sections.map((s) => s.name);
    names.forEach((n) => {
      if (!structure.includes(n)) structure.push(n);
    });

    structure = structure.filter((n) => names.includes(n));
    updateSectionSelect();
    updateStructureUI();
    updateConfigPreview();
  }

  function updateStructureUI() {
    structureList.innerHTML = "";
    const sectionCounts = {};
    structure.forEach((name) => {
      sectionCounts[name] = (sectionCounts[name] || 0) + 1;
    });
    const names = sections.map((s) => s.name || "");
    structure.forEach((name, idx) => {
      const div = document.createElement("div");
      div.className = "structure-item";
      div.setAttribute("draggable", "true");
      div.style.display = "flex";
      div.style.alignItems = "center";
      div.style.gap = "0.5em";

      const dragHandle = document.createElement("span");
      dragHandle.className = "drag-handle";
      dragHandle.title = "Drag to reorder";
      dragHandle.innerHTML = "&#9776;";
      div.appendChild(dragHandle);

      const textSpan = document.createElement("span");
      textSpan.textContent = `${idx + 1}. ${name}`;
      div.appendChild(textSpan);

      const count = structure.filter((n) => n === name).length;
      const canRemove = count > 1;
      const removeBtn = document.createElement("button");
      removeBtn.textContent = "Remove";
      removeBtn.className = "remove-btn";
      removeBtn.disabled = !canRemove;
      removeBtn.onclick = () => {
        if (canRemove) {
          structure.splice(idx, 1);
          updateStructureUI();
        }
      };
      div.appendChild(removeBtn);

      const moveCol = document.createElement("div");
      moveCol.style.display = "flex";
      moveCol.style.flexDirection = "column";
      moveCol.style.gap = "2px";
      moveCol.style.marginLeft = "0.5em";

      const upBtn = document.createElement("button");
      upBtn.textContent = "▲";
      upBtn.title = "Move up";
      upBtn.className = "move-btn";
      upBtn.disabled = idx === 0;
      upBtn.style.fontSize = "0.8em";
      upBtn.onclick = () => {
        if (idx > 0) {
          [structure[idx - 1], structure[idx]] = [
            structure[idx],
            structure[idx - 1],
          ];
          updateStructureUI();
        }
      };

      const downBtn = document.createElement("button");
      downBtn.textContent = "▼";
      downBtn.title = "Move down";
      downBtn.className = "move-btn";
      downBtn.disabled = idx === structure.length - 1;
      downBtn.style.fontSize = "0.8em";
      downBtn.onclick = () => {
        if (idx < structure.length - 1) {
          [structure[idx + 1], structure[idx]] = [
            structure[idx],
            structure[idx + 1],
          ];
          updateStructureUI();
        }
      };
      moveCol.appendChild(upBtn);
      moveCol.appendChild(downBtn);
      div.appendChild(moveCol);

      div.addEventListener("dragstart", (e) => {
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", idx);
        div.classList.add("dragging");
      });
      div.addEventListener("dragend", () => {
        div.classList.remove("dragging");
      });
      div.addEventListener("dragover", (e) => {
        e.preventDefault();
        div.classList.add("drag-over");
      });
      div.addEventListener("dragleave", () => {
        div.classList.remove("drag-over");
      });
      div.addEventListener("drop", (e) => {
        e.preventDefault();
        div.classList.remove("drag-over");
        const fromIdx = parseInt(e.dataTransfer.getData("text/plain"));
        if (fromIdx !== idx) {
          const moved = structure.splice(fromIdx, 1)[0];
          structure.splice(idx, 0, moved);
          updateStructureUI();
        }
      });
      structureList.appendChild(div);
    });

    setTimeout(updateConfigPreview, 0);
  }

  addToStructureBtn.onclick = null;
  addToStructureBtn.replaceWith(addToStructureBtn.cloneNode(true));
  const newAddBtn = document.getElementById("add-to-structure-btn");
  let sectionSelect = document.createElement("select");
  sectionSelect.id = "section-select-to-add";
  newAddBtn.parentNode.insertBefore(sectionSelect, newAddBtn);
  newAddBtn.textContent = "Add Section to Structure";
  newAddBtn.onclick = () => {
    const sel = sectionSelect.value;
    if (sel) {
      structure.push(sel);
      updateStructureUI();
      updateConfigPreview();
    }
  };
  function updateSectionSelect() {
    sectionSelect.innerHTML = "";
    sections.forEach((s) => {
      const opt = document.createElement("option");
      opt.value = s.name;
      opt.textContent = s.name;
      sectionSelect.appendChild(opt);
    });
  }

  function updateSectionUI() {
    if (sameForAll.checked) {
      addSectionBtn.style.display = "none";
      renderSections([sections[0]]);
    } else {
      addSectionBtn.style.display = "";
      renderSections(sections);
    }

    const names = sections.map((s) => s.name);
    names.forEach((n) => {
      if (!structure.includes(n)) structure.push(n);
    });

    structure = structure.filter((n) => names.includes(n));
    updateSectionSelect();
    updateStructureUI();
    updateConfigPreview();
  }

  function updateConfigPreview() {
    let sectionData = sameForAll.checked
      ? [getSectionsFromForm()[0]]
      : getSectionsFromForm();

    const names = sectionData.map((s) => s.name);
    structure = structure.filter((n) => names.includes(n));
    if (structure.length === 0 && names.length > 0) structure = [names[0]];
    const config = { structure, sections: sectionData };
    configPreview.textContent = JSON.stringify(config, null, 2);
  }

  downloadConfigBtn.onclick = function () {
    let sectionData = sameForAll.checked
      ? [getSectionsFromForm()[0]]
      : getSectionsFromForm();
    const config = { structure, sections: sectionData };
    const blob = new Blob([JSON.stringify(config, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "music_config.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const songForm = document.getElementById("song-form");

  let lastMusicUrl = null;
  let lastInfoUrl = null;
  function cleanupFiles() {
    if (lastMusicUrl || lastInfoUrl) {
      const payload = { files: [lastMusicUrl, lastInfoUrl].filter(Boolean) };

      let sent = false;
      try {
        if (navigator.sendBeacon && payload.files.length > 0) {
          const blob = new Blob([JSON.stringify(payload)], {
            type: "application/json",
          });
          sent = navigator.sendBeacon("/api/cleanup", blob);
        }
      } catch (e) {}

      if (!sent && payload.files.length > 0) {
        fetch("/api/cleanup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
          keepalive: true,
        });
      }
      lastMusicUrl = null;
      lastInfoUrl = null;
    }
  }

  window.addEventListener("beforeunload", cleanupFiles);

  songForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    cleanupFiles();
    let sectionData = sameForAll.checked
      ? [getSectionsFromForm()[0]]
      : getSectionsFromForm();
    const payload = { structure, sections: sectionData };
    const songInfo = document.getElementById("song-info");
    songInfo.innerHTML = "Generating music...";
    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!resp.ok) throw new Error("Music generation failed");
      const data = await resp.json();
      songInfo.innerHTML = `
                <button onclick="window.open('${data.music_url}', '_blank')" style="margin-bottom:0.5em;">Download Music</button>
                <button onclick="window.open('${data.info_url}', '_blank')" style="margin-bottom:0.5em;">Download Info</button><br><br>
                <div id="custom-audio-player" class="custom-audio-player" data-src="${data.music_url}"></div>
            `;

      setTimeout(() => {
        const playerDiv = document.getElementById("custom-audio-player");
        if (!playerDiv) return;
        const audio = document.createElement("audio");
        audio.src = playerDiv.getAttribute("data-src");
        audio.preload = "auto";
        audio.style.display = "none";
        playerDiv.appendChild(audio);

        playerDiv.innerHTML += `
                  <div class="cap-controls">
                    <button class="cap-play" title="Play">&#9654;</button>
                    <button class="cap-pause" style="display:none;" title="Pause">&#10073;&#10073;</button>
                    <input type="range" class="cap-progress" min="0" max="100" value="0" step="0.1">
                    <span class="cap-time">0:00 / 0:00</span>
                    <div class="cap-volume-wrap">
                      <button class="cap-volume-btn" title="Volume">&#128266;</button>
                      <input type="range" class="cap-volume" min="0" max="1" value="0.5" step="0.01" title="Volume">
                    </div>
                  </div>
                `;
        const playBtn = playerDiv.querySelector(".cap-play");
        const pauseBtn = playerDiv.querySelector(".cap-pause");
        const progress = playerDiv.querySelector(".cap-progress");
        const volume = playerDiv.querySelector(".cap-volume");
        const volumeBtn = playerDiv.querySelector(".cap-volume-btn");
        const volumeWrap = playerDiv.querySelector(".cap-volume-wrap");
        const time = playerDiv.querySelector(".cap-time");

        audio.volume = 0.5;
        volume.value = 0.5;

        playBtn.onclick = () => {
          audio.play();
        };
        pauseBtn.onclick = () => {
          audio.pause();
        };
        audio.addEventListener("play", () => {
          playBtn.style.display = "none";
          pauseBtn.style.display = "";
        });
        audio.addEventListener("pause", () => {
          playBtn.style.display = "";
          pauseBtn.style.display = "none";
        });

        audio.addEventListener("timeupdate", () => {
          if (audio.duration) {
            progress.value = (
              (audio.currentTime / audio.duration) *
              100
            ).toString();
          } else {
            progress.value = "0";
          }
          time.textContent = `${formatTime(audio.currentTime)} / ${formatTime(
            audio.duration
          )}`;
        });
        progress.oninput = () => {
          if (audio.duration) {
            audio.currentTime = (progress.value / 100) * audio.duration;
          }
        };

        function showVolumeSlider() {
          volumeBtn.style.opacity = "0";
          volume.style.display = "inline-block";
          volume.focus();
        }
        function hideVolumeSlider() {
          volume.style.display = "none";
          volumeBtn.style.opacity = "1";
        }

        volumeWrap.addEventListener("mouseenter", showVolumeSlider);
        volumeWrap.addEventListener("mouseleave", hideVolumeSlider);
        volumeBtn.addEventListener("focus", showVolumeSlider);
        volumeBtn.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") showVolumeSlider();
        });
        volume.addEventListener("blur", hideVolumeSlider);
        volume.addEventListener("keydown", (e) => {
          if (e.key === "Escape") hideVolumeSlider();
        });

        volume.oninput = () => {
          audio.volume = volume.value;
        };

        function formatTime(sec) {
          if (!isFinite(sec)) return "0:00";
          const m = Math.floor(sec / 60);
          const s = Math.floor(sec % 60);
          return `${m}:${s.toString().padStart(2, "0")}`;
        }
      }, 0);

      lastMusicUrl = data.music_url;
      lastInfoUrl = data.info_url;

      if (data.music_file_url) lastMusicUrl = data.music_file_url;
      if (data.info_file_url) lastInfoUrl = data.info_file_url;
    } catch (err) {
      songInfo.innerHTML = "Error: " + err.message;
    }
  });

  addSectionBtn.addEventListener("click", () => {
    sections.push({
      name: `Section ${sections.length + 1}`,
      duration: 4,
      instruments: ["__random__"],
      drums: ["__random__"],
      effects: ["__random__"],
    });
    updateSectionUI();
  });
  sameForAll.addEventListener("change", updateSectionUI);
  updateSectionUI();
});
