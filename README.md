<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RuVl/MatMex-Week">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MatMex Week Bot</h3>

  <p align="center">
    Bot for mathmech week
    <br />
    <a href="https://github.com/RuVl/MatMex-Week"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/RuVl/MatMex-Week">View Demo</a>
    &middot;
    <a href="https://github.com/RuVl/MatMex-Week/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/RuVl/MatMex-Week/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Данный бот предназначен для недели Матмеха. В его функции входят регистрация новых участников недели, начисление валюты за участие в событиях, магазин мерча, администрирование пользователей.
Сам бот обернут в докер и сопровождается postgres и redis.
Trello: [https://trello.com/b/rDOuwQsR/matmex-week](https://trello.com/b/rDOuwQsR/matmex-week)
Схема базы данных: [https://dbdiagram.io/d/67f003894f7afba184640672](https://dbdiagram.io/d/67f003894f7afba184640672)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![Docker][Docker.com]][Docker-url]
* [![Postgres][Postgres.org]][Postgres-url]
* [![Redis][Redis.io]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

How to launch bot

### Prerequisites

* docker [https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository](Instruction_for_Ubuntu)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/RuVl/MatMex-Week.git
   ```
2. Set environment variables

3. Run docker compose
   ```sh
   docker compose up
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request to branch dev

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/RuVl/MatMex-Week/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=RuVl/MatMex-Week" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/RuVl/MatMex-Week](https://github.com/RuVl/MatMex-Week)

Docker Hub: ...?

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/RuVl/MatMex-Week.svg?style=for-the-badge
[contributors-url]: https://github.com/RuVl/MatMex-Week/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RuVl/MatMex-Week.svg?style=for-the-badge
[forks-url]: https://github.com/RuVl/MatMex-Week/network/members
[stars-shield]: https://img.shields.io/github/stars/RuVl/MatMex-Week.svg?style=for-the-badge
[stars-url]: https://github.com/RuVl/MatMex-Week/stargazers
[issues-shield]: https://img.shields.io/github/issues/RuVl/MatMex-Week.svg?style=for-the-badge
[issues-url]: https://github.com/RuVl/MatMex-Week/issues
[license-shield]: https://img.shields.io/github/license/RuVl/MatMex-Week.svg?style=for-the-badge
[license-url]: https://github.com/RuVl/MatMex-Week/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png

[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://python.org
[Docker.com]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://docker.com
[Postgres.org]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://postgresql.org
[Redis.io]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io 
