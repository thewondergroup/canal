/* CANAL — site settings. The only file the team should need to touch. */
window.CANAL = {
  // Google Sheet for the menus: File > Share > Publish to web > (menu tab) > CSV, paste the link here.
  // Leave empty to use data/menu.csv in the repo.
  menuSheetCsv: "",

  // Opening hours (24h, Europe/London). 0 = Sunday.
  hours: {
    0: ["12:00", "20:30"],
    1: ["12:00", "22:00"], 2: ["12:00", "22:00"], 3: ["12:00", "22:00"],
    4: ["12:00", "22:00"], 5: ["12:00", "22:00"], 6: ["12:00", "22:00"]
  },
  // Days the restaurant is closed, as YYYY-MM-DD (e.g. Boxing Day).
  closedDates: [],

  // For sunset + weather (Woodfield Road, W9)
  lat: 51.5207, lng: -0.2006
};
