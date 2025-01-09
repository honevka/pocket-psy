<template>
  <v-app>
    <v-container max-width="1300">
      <v-card max-width="300">
        <v-container>
          <div class="d-flex align-center justify-center">
            <v-img
              fluid
              src="../src/assets/diary.png"
              alt="Дневник эмоций"
              max-width="40"
              contain
            ></v-img>

            <v-card-title class="custom-title">Дневник эмоций</v-card-title>
          </div>

          <div class="d-flex justify-center">
            <v-dialog max-width="500" v-model="dialogEmotions">
              <template v-slot:activator="{ props: activatorProps }">
                <v-btn
                  color="black"
                  v-bind="activatorProps"
                  text="Добавить запись"
                  class="btn-add-note mt-3"
                ></v-btn>
              </template>

              <template v-slot:default="{ isActive }">
                <div>
                  <v-card title="Эмоции">
                    <v-card-text>
                      Выбери эмоции, которые ты испытываешь:

                      <v-chip-group
                        v-model="selectedEmotion"
                        multiple
                        class="d-flex flex-wrap"
                        column
                      >
                        <v-chip
                          v-for="(field, index) in emotions"
                          :key="index"
                          :text="field.name"
                          :value="field.id"
                          variant="outlined"
                          filter
                          class="ma-1"
                        ></v-chip>
                      </v-chip-group>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn text="Закрыть" @click="deleteEmotionsData"></v-btn>
                      <v-btn
                        text="Продолжить"
                        @click="getDialogSituation"
                      ></v-btn>
                    </v-card-actions>
                  </v-card>
                </div>
              </template>
            </v-dialog>
          </div>
          <div class="d-flex justify-center">
            <v-dialog max-width="500" v-model="dialogSituation">
              <v-card title="Ситуация и мысли">
                <v-card-text>
                  Если ты испытываешь сильные эмоции, пожалуйста, сделай сначала
                  практики, чтобы снизить их интенсивность: *ссылка*
                </v-card-text>
                <v-card-text> Какая ситуация вызвала эти эмоции? </v-card-text>
                <v-textarea
                  label="Ситуация"
                  variant="outlined"
                  class="mx-5"
                  v-model="newNote.situation"
                ></v-textarea>
                <v-card-text>
                  Какие у тебя были/есть негативные мысли?
                </v-card-text>
                <v-textarea
                  label="Мои негативные мысли"
                  variant="outlined"
                  class="mx-5"
                  v-model="newNote.thoughts"
                ></v-textarea>

                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn text="Назад" @click="dialogSituation = false"></v-btn>
                  <v-btn text="Закрыть" @click="deleteEmotionsData"></v-btn>
                  <v-btn text="Продолжить" @click="getDialogSupport"></v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>

          <div class="d-flex justify-center">
            <v-dialog max-width="500" v-model="dialogSupport">
              <v-card title="Поддержка">
                <v-card-text>
                  Какие глубинные убеждения есть?

                  <v-chip-group
                    v-model="selectedConviction"
                    multiple
                    class="d-flex flex-wrap"
                    column
                  >
                    <v-chip
                      v-for="(field, index) in convictions"
                      :key="index"
                      :text="field.name"
                      :value="field.id"
                      variant="outlined"
                      filter
                      class="ma-1"
                    ></v-chip>
                  </v-chip-group>
                </v-card-text>
                <v-card-text>
                  Какие когнитивные искажения есть? Про искажения подробнее по
                  ссылке *ссылка*
                  <v-chip-group
                    v-model="selectedDistortion"
                    multiple
                    class="d-flex flex-wrap"
                    column
                  >
                    <v-chip
                      v-for="(field, index) in distortions"
                      :key="index"
                      :text="field.name"
                      :value="field.value"
                      variant="outlined"
                      filter
                      class="ma-1"
                    ></v-chip>
                  </v-chip-group>
                </v-card-text>

                <v-card-text>
                  Опровергни глубинные убеждения, обрати внимание на искажения и
                  поддержи себя
                </v-card-text>
                <v-textarea
                  label="Поддержи себя"
                  variant="outlined"
                  class="mx-5"
                  v-model="newNote.support"
                ></v-textarea>
                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn text="Назад" @click="dialogSituation = false"></v-btn>
                  <v-btn text="Закрыть" @click="deleteEmotionsData"></v-btn>
                  <v-btn text="Сохранить" @click="addNote"></v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
        </v-container>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    dialogSupport: false,
    newNoteEmotion: { },
    newNote: {
    },
    notes: [],
    note_emotions: [],
    note_convictions: [],
    selectedEmotion: null,
    selectedConviction: null,
    dialogDistortions1: false,
    dialogDistortions2: false,
    dialogSituation: false,
    dialogEmotions: false,
    selectedEmotions: [],
    selectedDistortion: [],
    distortions: [],
    emotions: [],
    convictions: [],
    newNoteConviction: {},
  }),
  head() {
    return {
      title: "Мое Nuxt приложение",
    };
  },
  mounted() {
    this.getEmotions();
    this.getConvictions();
    this.getDistortions();
  },
  methods: {
    async getDistortions() {
      try {
        const response = await fetch("http://localhost:8000/distortions/");
        this.distortions = await response.json();
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    },
    async getEmotions() {
      try {
        const response = await fetch("http://localhost:8000/emotions/");
        this.emotions = await response.json();
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    },
    async getConvictions() {
      try {
        const response = await fetch("http://localhost:8000/convictions/");
        this.convictions = await response.json();
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    },
    async addNote() {
      const response = await fetch("http://localhost:8000/notes/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.newNote),
      });
      const note = await response.json();
      this.notes.push(note);

      this.selectedEmotion.forEach(async (element) => {
        this.newNoteEmotion.emotion_id = element
        this.newNoteEmotion.note_id = note.id
        const response = await fetch("http://localhost:8000/note_emotions/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.newNoteEmotion),
        });
        const note_emotion = await response.json();
        this.note_emotions.push(note_emotion);

      });
      this.selectedConviction.forEach(async (elementConviction) => {
        this.newNoteConviction.conviction_id = elementConviction
        this.newNoteConviction.note_id = note.id
        const response = await fetch("http://localhost:8000/note_convictions/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.newNoteConviction),
        });
        const note_conviction = await response.json();
        this.note_convictions.push(note_conviction);
        this.newNoteEmotion = {}
        this.newNote = {}
        this.newNoteConviction = {}
      });

    },
    async getDialogSupport() {
      this.dialogSituation = false;
      this.dialogSupport = true;
    },
    async deleteEmotionsData() {
      this.dialogEmotions = false;
      this.dialogSituation = false;
      this.selectedEmotion = null;
      this.selectedEmotions = [];
      this.dialogSupport = false;
    },
    async getDialogSituation() {
      console.log("this.selectedEmotion");
      console.log(this.selectedEmotion);
      this.dialogSituation = true;
      this.dialogEmotions = false;
    },

    async getListSelectedEmotions() {
      this.selectedEmotions = [];
      if (this.selectedEmotion != null) {
        this.selectedEmotion.forEach(async (element) => {
          this.emotions.fields.forEach(async (emotion) => {
            if (emotion.value === element) {
              console.log("emotion.value:", emotion.value);
              console.log("element:", element);

              // Убедитесь, что selectedEmotions - это массив
              console.log("this.selectedEmotions:", this.selectedEmotions);

              this.selectedEmotions.push({
                text: emotion.name,
                value: emotion.value,
              });
              console.log("Updated selectedEmotions:", this.selectedEmotions);
            }
          });
        });
      }
    },
  },
};
</script>
<style>
.custom-title {
  font-weight: bold; /* Делает шрифт жирным */
  font-size: 28px; /* Увеличивает размер шрифта */
}
.btn-add-note {
  background-color: black;
}
.v-main {
  background-color: #f6f6f6;
}
.v-application__wrap {
  background-color: #f6f6f6;
}
</style>
