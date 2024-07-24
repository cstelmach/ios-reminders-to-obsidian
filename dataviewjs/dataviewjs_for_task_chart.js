// Completed Tasks Chart Generator
// This script generates a chart of completed tasks from daily notes in Obsidian

// Constants
const DAYS_TO_SHOW = 15; // Number of days to display in the chart

// Task Categories
const TASK_CATEGORIES = {
  "task(today).imp": {
    remindersLists: ["task(today).imp", "task(...time).imp"],
    backgroundColor: "rgba(189, 42, 28, 0.5)",
    borderColor: "#BD2A1C",
  },
  "task(today)": {
    remindersLists: ["task(today)", "task(...time)"],
    backgroundColor: "rgba(219, 166, 3, 0.5)",
    borderColor: "#DBA603",
  },
  "task(area)": {
    remindersLists: ["task(...time)", "task(...time)"],
    backgroundColor: "rgba(219, 166, 3, 0.5)",
    borderColor: "#DBA603",
  },
  Code: {
    remindersLists: ["task(code)", /proj\(.*\)/i, /code\(.*\)/i],
    backgroundColor: "rgba(172, 101, 215, 0.5)",
    borderColor: "#AC65D7",
  },
  Learn: {
    remindersLists: [/learn\(.*\)/i, /code\(.*\)/i],
    backgroundColor: "rgba(93, 144, 214, 0.5)",
    borderColor: "#5D90D6",
  },
  Ideas: {
    remindersLists: [/ideas\(.*\)/i, /download\(.*\)/i],
    backgroundColor: "rgba(255, 234, 120, 0.5)",
    borderColor: "#FFEA78",
  },
  Work: {
    remindersLists: [/work\(.*\)/i, /.*employment.*/],
    backgroundColor: "rgba(177, 134, 83, 0.5)",
    borderColor: "#B18653",
  },
  Secure: {
    remindersLists: [/secure\(.*\)/i],
    backgroundColor: "rgba(250, 199, 250, 0.5)",
    borderColor: "#FAC7FA",
  },
  Uncategorized: {
    remindersLists: [],
    backgroundColor: "rgba(158, 158, 158, 0.5)",
    borderColor: "#9e9e9e",
  },
};

// Helper Functions
function extractDateFromFilename(filename) {
  const regex = /^JD (\d{8})/;
  const match = filename.match(regex);
  if (match) {
    return moment(match[1], "YYYYMMDD");
  }
  return null;
}

function categorizeTaskList(name, categories) {
  for (let category in categories) {
    for (let pattern of categories[category].remindersLists) {
      if (typeof pattern === "string" && name.includes(pattern)) {
        return category;
      }
      if (pattern instanceof RegExp && pattern.test(name)) {
        return category;
      }
    }
  }
  return "Uncategorized";
}

async function countCompletedTasks(content, categories) {
  let lines = content.split("\n");
  let inCompletedTasksSection = false;
  let header = null;
  let categoryTaskCounts = {};

  for (let line of lines) {
    if (line.startsWith("## ")) {
      if (line.trim() === "## Completed Tasks") {
        inCompletedTasksSection = true;
      } else {
        inCompletedTasksSection = false;
      }
      header = null;
    } else if (inCompletedTasksSection && line.startsWith("### ")) {
      header = line.replace("### ", "").trim();
      let category = categorizeTaskList(header, categories);
      if (!categoryTaskCounts[category]) {
        categoryTaskCounts[category] = 0;
      }
    } else if (
      inCompletedTasksSection &&
      header &&
      line.match(/^\s*- \[x\]/)
    ) {
      let category = categorizeTaskList(header, categories);
      categoryTaskCounts[category] += 1;
    }
  }
  return categoryTaskCounts;
}

function getDateRange(currentNoteMoment, today) {
  let startDate, endDate;
  const halfRange = Math.floor((DAYS_TO_SHOW - 1) / 2);

  if (today.diff(currentNoteMoment, "days") <= halfRange) {
    startDate = currentNoteMoment
      .clone()
      .subtract(DAYS_TO_SHOW - today.diff(currentNoteMoment, "days") - 1, "days");
    endDate = today;
  } else {
    startDate = currentNoteMoment.clone().subtract(halfRange, "days");
    endDate = currentNoteMoment.clone().add(halfRange, "days");
  }

  return { startDate, endDate };
}

function prepareChartData(labels, dateCategoryCounts, categories) {
  return Object.keys(categories).map((category) => {
    return {
      label: category,
      data: labels.map((label) =>
        dateCategoryCounts[label]
          ? dateCategoryCounts[label][category] || 0
          : 0
      ),
      backgroundColor: categories[category].backgroundColor,
      borderColor: categories[category].borderColor,
      borderWidth: 2,
    };
  });
}

function getChartSettings(labels, datasets, currentNoteMoment, today) {
  const isMobile = app.isMobile;
  const vaultName = app.vault.getName();
  const folderName = "journal/day/";

  function openObsidianNote(date) {
    const fileName = date.format("J[D] YYYYMMDD");
    const urlEncodedFolderName = encodeURIComponent(folderName);
    const urlEncodedFileName = encodeURIComponent(fileName);
    const link = `obsidian://open?vault=${vaultName}&file=${urlEncodedFolderName}${urlEncodedFileName}`;
    window.open(link, "_blank");
  }

  // Calculate the maximum total value across all days
  const totals = labels.map((_, index) =>
    datasets.reduce((sum, dataset) => sum + (dataset.data[index] || 0), 0)
  );
  let maxTotal = Math.max(...totals);

  // If maxTotal is 0, set it to 1 to ensure clickable areas
  if (maxTotal === 0) {
    maxTotal = 1;
  }

  // Create the invisible dataset
  const invisibleDataset = {
    label: "Invisible",
    data: totals.map((total) => Math.max(maxTotal - total, 1)), // Ensure at least 1 for clickability
    backgroundColor: "rgba(0, 0, 0, 0)",
    hoverBackgroundColor: "rgba(0, 0, 0, 0)",
    borderColor: "rgba(0, 0, 0, 0)",
    borderWidth: 0,
  };

  // Add the invisible dataset to the existing datasets
  const newDatasets = [...datasets, invisibleDataset];

  return {
    type: "bar",
    data: {
      labels: labels,
      datasets: newDatasets,
    },
    options: {
      animation: false,
      aspectRatio: isMobile ? 5 : 7,
      onClick: (event, elements, chart) => {
        if (elements.length > 0) {
          const index = elements[0].index;
          const date = moment(labels[index]);
          openObsidianNote(date);
        }
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          filter: (tooltipItem) => {
            // Filter out the invisible dataset from the tooltip
            return tooltipItem.datasetIndex !== newDatasets.length - 1;
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          stacked: true,
          position: "right",
          ticks: {
            stepSize: 1,
            callback: function (value) {
              return value === 0 ? "" : value;
            },
          },
          grid: {
            drawTicks: false,
            display: false,
            color: `rgba(150,150,150, 0.3)`,
            drawBorder: false,
          },
        },
        x: {
          type: "time",
          time: {
            unit: "day",
            tooltipFormat: "J[D] YYYYMMDD",
            displayFormats: {
              day: "dd",
            },
          },
          stacked: true,
          grid: {
            drawTicks: false,
            color: `rgba(150,150,150, 0.3)`,
          },
          ticks: {
            maxRotation: 0,
            minRotation: 0,
            align: "center",
            crossAlign: "near",
            callback: function (value, index, values) {
              let label = labels[index];
              let dateLabel = moment(label).format("dd");
              return dateLabel;
            },
            color: function (context) {
              let label = labels[context.index];
              if (label === currentNoteMoment.format("YYYY-MM-DD")) {
                return "#62D864"; // Green for current note
              } else if (label === today.format("YYYY-MM-DD")) {
                return "#24B5FC"; // Blue for today
              } else {
                return "rgb(150, 150, 150)"; // Standard color
              }
            },
            font: function (context) {
              let label = labels[context.index];
              if (
                label === currentNoteMoment.format("YYYY-MM-DD") ||
                label === today.format("YYYY-MM-DD")
              ) {
                return {
                  weight: "bold",
                };
              }
            },
          },
        },
      },
    },
  };
}

// Main Function
async function generateCompletedTasksBlock(dv) {
  // Get the current note's date
  const cp = dv.current();
  const currentNoteDate = cp.file.day;
  const currentNoteMoment = moment(currentNoteDate.toISODate());

  // Get today's date
  const today = moment();

  // Calculate the date range for the chart
  const { startDate, endDate } = getDateRange(currentNoteMoment, today);

  // Get the notes within the date range
  let dailyNotes = dv
    .pages(`"journal/day"`)
    .filter((n) =>
      moment(n.file.day).isBetween(startDate, endDate, null, "[]")
    )
    .sort((b) => b.file.ctime, "desc");

  // Create an array to hold the counts of completed tasks for each note and header
  let completedTaskCounts = [];

  // Iterate through each note
  for (let note of dailyNotes) {
    try {
      // Extract the date from the filename or use the creation date
      let noteDate =
        extractDateFromFilename(note.file.name) ||
        moment(note.file.ctime);

      // Get the content of the note
      let content = await dv.io.load(note.file.path);

      // Count completed tasks under each header in the note content
      let categoryTaskCounts = await countCompletedTasks(
        content,
        TASK_CATEGORIES
      );

      // Add the note's title, date, and the category task counts to the array
      completedTaskCounts.push({
        title: note.file.name,
        date: noteDate,
        categories: categoryTaskCounts,
      });
    } catch (error) {
      console.error(`Error processing note ${note.file.name}:`, error);
    }
  }

  // Aggregate the completed tasks by date and category
  let dateCategoryCounts = {};
  completedTaskCounts.forEach((note) => {
    let date = note.date.format("YYYY-MM-DD");
    if (!dateCategoryCounts[date]) {
      dateCategoryCounts[date] = {};
    }
    for (let category in note.categories) {
      if (!dateCategoryCounts[date][category]) {
        dateCategoryCounts[date][category] = 0;
      }
      dateCategoryCounts[date][category] += note.categories[category];
    }
  });

  // Prepare data for the chart
  let labels = [];
  for (
    let m = startDate.clone();
    m.isSameOrBefore(endDate);
    m.add(1, "days")
  ) {
    labels.push(m.format("YYYY-MM-DD"));
  }

  let datasets = prepareChartData(labels, dateCategoryCounts, TASK_CATEGORIES);

  // Create the chart element
  let chartEl = dv.el("chart__completed-tasks", "");

  // Get chart settings
  let chartSettings = getChartSettings(labels, datasets, currentNoteMoment, today);

  // Render the chart using the Charts plugin
  await window.renderChart(chartSettings, chartEl);
}

// Export the main function
// module.exports = generateCompletedTasksBlock;

// Run the main function (add this to a dataviewjs block in your note)
generateCompletedTasksBlock(dv);