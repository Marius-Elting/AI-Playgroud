import Link from 'next/link';
import styles from "./page.module.scss";

export default function Home() {
  return (
    <div className={styles.page}>
        <main className={styles.main}>
            <h1>Welcome to my AI Playground</h1>
            <p>Here I test some OpeanAI functionalities and others.</p>
            <ul>
                <Link href="/chat">CHAT</Link>
            </ul>
        </main>
    </div>
  );
}
