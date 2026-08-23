/*
  Public catalog: what students see. Stubs stay in the database (admin still
  lists them). Expand a1Public as complete free A1 lessons go live.
*/

window.EnglishPathCatalog = (function () {
  const A1_PUBLIC_COVERS = new Set(["to-be", "have-got"]);
  const A1_PUBLIC_IDS = new Set([209]);
  const A1_PUBLIC_SECTIONS = new Set(["grammar"]);

  function isA1PublicLesson(lesson) {
    if (!lesson) return false;
    if (A1_PUBLIC_IDS.has(Number(lesson.id))) return true;
    const cover = String(lesson.cover_key || "");
    if (A1_PUBLIC_COVERS.has(cover)) return true;
    const title = String(lesson.title || "");
    if (/have got/i.test(title)) return true;
    if (/forms of ['']to be['']/i.test(title)) return true;
    return false;
  }

  /** Section grids: A1 shows only the finished lessons; other levels unchanged. */
  function isListedOnSection(lesson, levelId) {
    const level = String(levelId || lesson?.level || "").toLowerCase();
    if (level !== "a1") return true;
    return isA1PublicLesson(lesson);
  }

  /** A1 level page: only sections that currently have public lessons. */
  function sectionsForLevel(levelId, allSections) {
    const list = Array.isArray(allSections) ? allSections : [];
    if (String(levelId || "").toLowerCase() !== "a1") return list;
    return list.filter((s) => A1_PUBLIC_SECTIONS.has(s.id));
  }

  return {
    isA1PublicLesson,
    isListedOnSection,
    sectionsForLevel,
  };
})();
