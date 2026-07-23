use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;
use sha2::{Digest, Sha256};
use serde::Serialize;
use walkdir::WalkDir;

#[derive(Serialize)]
struct FileEntry {
    rel_path: String,
    size_bytes: u64,
    sha256: String,
    git_status: String,
}

#[derive(Serialize)]
struct ManifestReport {
    generated_utc: String,
    repo_root: String,
    total_files: usize,
    elapsed_ms: u128,
    files: Vec<FileEntry>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start = Instant::now();
    let cwd = env::current_dir()?;

    // 1. Discover Git Repository using gitoxide (gix)
    let repo = gix::discover(&cwd)?;
    let work_dir = repo
        .work_dir()
        .ok_or("Bare repository not supported")?
        .to_path_buf();

    // 2. Load Git Index in-memory
    let index = repo.index_or_empty()?;

    let mut entries = Vec::new();

    // 3. Fast Walk workspace tree
    for entry in WalkDir::new(&work_dir)
        .into_iter()
        .filter_entry(|e| {
            let name = e.file_name().to_string_lossy();
            name != ".git" 
                && name != "target" 
                && name != "build" 
                && name != "node_modules" 
                && name != ".venv"
        })
    {
        let entry = match entry {
            Ok(e) => e,
            Err(_) => continue,
        };

        if !entry.file_type().is_file() {
            continue;
        }

        let path = entry.path();
        let rel_path = match path.strip_prefix(&work_dir) {
            Ok(p) => p.to_string_lossy().to_string(),
            Err(_) => continue,
        };

        if rel_path == "manifest.json" || rel_path.starts_with("gemini/captures/") {
            continue;
        }

        let metadata = match fs::metadata(path) {
            Ok(m) => m,
            Err(_) => continue,
        };

        // 4. In-Memory Index Match via bstr
        let path_bytes = rel_path.as_bytes();
        let is_tracked = index.entry_by_path(path_bytes.into()).is_some();

        // 5. Fast SHA-256 Hashing
        let sha256 = if metadata.len() <= 100 * 1024 * 1024 {
            match fs::read(path) {
                Ok(bytes) => format!("{:x}", Sha256::digest(&bytes)),
                Err(_) => "READ_ERROR".to_string(),
            }
        } else {
            "SKIPPED_TOO_LARGE".to_string()
        };

        entries.push(FileEntry {
            rel_path,
            size_bytes: metadata.len(),
            sha256,
            git_status: if is_tracked { "tracked" } else { "untracked_or_ignored" }.to_string(),
        });
    }

    let elapsed = start.elapsed().as_millis();

    println!("================================================================================");
    println!(" GIX_MANIFEST: RUST GITOXIDE FAST WORKSPACE SCANNER");
    println!("================================================================================");
    println!(" Repo Root    : {}", work_dir.display());
    println!(" Total Files  : {}", entries.len());
    println!(" Execution    : {} ms (Blazing Fast!)", elapsed);
    println!("================================================================================");

    let report = ManifestReport {
        generated_utc: chrono::Utc::now().to_rfc3339(),
        repo_root: work_dir.to_string_lossy().to_string(),
        total_files: entries.len(),
        elapsed_ms: elapsed,
        files: entries,
    };

    let output_path = work_dir.join("gemini").join("captures").join("gix_manifest.json");
    if let Some(parent) = output_path.parent() {
        fs::create_dir_all(parent)?;
    }
    fs::write(&output_path, serde_json::to_string_pretty(&report)?)?;

    println!(" Report Written To: {}", output_path.display());
    println!("================================================================================");

    Ok(())
}
