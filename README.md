

# Press Information Bureau (PIB) Daily Summary Web App

![PIB Daily Summary Web App Demo](./images/image.png)

## Project Essence

This web app is designed to help students preparing for competitive exams (like UPSC, State PSCs, SSC, etc.) save valuable time in current affairs note-making. It automatically fetches daily press releases from the Press Information Bureau (PIB), summarizes them using advanced AI models (Large Language Models, LLMs), and presents the key points in a concise, student-friendly format. Each summary is tagged by topic and ministry, with abbreviations expanded for clarity, making revision and topic tracking effortless.

## AI & LLM Usage

- **Automated Summarization:** The backend leverages state-of-the-art AI and LLMs (such as OpenAI's GPT models and DeepSeek) to generate short, clear, and exam-focused summaries from raw PIB articles.
- **Tag Generation:** AI is also used to extract and expand relevant tags and abbreviations, making it easier to organize and search content.
- **Flexible LLM Integration:** The system supports both OpenAI and OpenRouter/DeepSeek APIs, making it adaptable to different AI providers.

## Web Development Aspects

- **Modern Frontend:** Built with HTML, CSS, and JavaScript, the frontend displays summaries as sticky-note style cards in a responsive grid layout, ensuring a smooth experience on all devices.
- **Seamless Data Flow:** The backend pipeline automates scraping, summarization, tagging, and storage in local JSON files, which the frontend fetches and displays by date.
- **User Experience:** Features like date selection, tag display, and error handling make the app practical and user-friendly for exam aspirants.

## How It Helps Students

- **Saves Time:** No more manual reading and summarizing of lengthy PIB articles—get ready-to-use, bullet-point notes every day.
- **Student-Friendly Summaries:** AI-generated summaries are short, clear, and focused on what matters for exams.
- **Easy Tagging & Filtering:** Summaries are tagged by ministry and topic, helping you quickly find and revise relevant content.
- **Modern, Responsive UI:** Sticky-note style cards make browsing summaries enjoyable on any device.
- **Open Source & Local:** All data is stored locally in JSON files—no login or cloud required.

## Call for Community Contributions

This project is open source and welcomes contributions! Whether you are a developer, designer, educator, or exam aspirant, your ideas and improvements can help make this tool even more useful. Possible areas for contribution:

- Improving the AI summarization or tagging logic
- Enhancing the UI/UX for better readability and accessibility
- Adding new features (search, export, notifications, etc.)
- Expanding to other sources or exam types

Feel free to fork, suggest features, or submit pull requests. Together, we can build a smarter, time-saving resource for all exam aspirants!
