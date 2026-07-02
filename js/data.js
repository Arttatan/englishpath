/*
  Central site data: levels and sections.
  Used on the home page and on level pages.
  Change it here and the navigation updates across the whole site.
*/

window.SITE = {
  // Site name. Change it in this one place and it updates everywhere.
  brand: "EnglishPath",

  // CEFR levels
  levels: [
    {
      id: "a1",
      title: "A1",
      subtitle: "Beginner",
      description: "The very first level: simple phrases, basic grammar and everyday words.",
      color: "#22c55e",
    },
    {
      id: "a2",
      title: "A2",
      subtitle: "Elementary",
      description: "Everyday situations, past and future tenses, and a wider vocabulary.",
      color: "#10b981",
    },
    {
      id: "b1",
      title: "B1",
      subtitle: "Intermediate",
      description: "Confident communication on familiar topics, harder grammar and texts.",
      color: "#3b82f6",
    },
    {
      id: "b1plus",
      title: "B1+",
      subtitle: "Upper-Intermediate (entry)",
      description: "A bridge level: getting ready for more advanced structures and texts.",
      color: "#6366f1",
    },
    {
      id: "b2",
      title: "B2",
      subtitle: "Upper-Intermediate",
      description: "Fluent communication, abstract topics and complex grammar structures.",
      color: "#8b5cf6",
    },
    {
      id: "c1",
      title: "C1",
      subtitle: "Advanced",
      description: "Near-native precision: nuanced grammar, academic texts and sophisticated vocabulary.",
      color: "#ec4899",
    },
  ],

  // Sections inside every level
  sections: [
    {
      id: "grammar",
      title: "Grammar",
      en: "Grammar",
      icon: "📘",
      description: "Clear rule explanations with examples and exercises.",
    },
    {
      id: "vocabulary",
      title: "Vocabulary",
      en: "Vocabulary",
      icon: "🗂️",
      description: "New words and expressions by topic with practice.",
    },
    {
      id: "listening",
      title: "Listening",
      en: "Listening",
      icon: "🎧",
      description: "Audio recordings with comprehension tasks.",
    },
    {
      id: "reading",
      title: "Reading",
      en: "Reading",
      icon: "📖",
      description: "Texts of different levels with comprehension questions.",
    },
    {
      id: "use-of-english",
      title: "Use of English",
      en: "Use of English",
      icon: "🧩",
      description: "Combined tasks on grammar and vocabulary together.",
    },
    {
      id: "writing",
      title: "Writing",
      en: "Writing",
      icon: "✍️",
      description: "How to write letters, essays and messages in English.",
    },
  ],

  // How many lessons are free (used in later steps)
  freeLessonsLimit: 3,

  // Subscription price (for display)
  price: "$5",
};
