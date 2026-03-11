<template>
    <div class="profile-container">
        <h2>Student Profile</h2>
        
        <!-- Loading State -->
        <div v-if="loading" class="loading">
            Loading your profile...
        </div>

        <!-- Profile Exists - Display Only -->
        <div v-else-if="profileExists && profileLoaded" class="profile-display">
            <div class="card">
                <h3 class="text-primary">Your Profile Information</h3>
                
                <div class="profile-grid">
                    <div class="profile-item">
                        <span class="profile-label">Full Name</span>
                        <span class="profile-value">{{ profile.full_name }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">Email</span>
                        <span class="profile-value">{{ profile.email }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">Branch</span>
                        <span class="profile-value">{{ profile.branch }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">CGPA</span>
                        <span class="profile-value">{{ profile.cgpa }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">Graduation Year</span>
                        <span class="profile-value">{{ profile.graduation_year }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">Skills</span>
                        <span class="profile-value">{{ profile.skills }}</span>
                    </div>
                    
                    <div class="profile-item">
                        <span class="profile-label">Resume</span>
                        <a :href="profile.resume" target="_blank" class="profile-link">View Resume</a>
                    </div>
                </div>

                <div class="profile-actions">
                    <button @click="toggleEditMode()" class="btn-primary">✏️ Edit Profile</button>
                </div>
            </div>
        </div>

        <!-- Edit Mode - Show Form -->
        <div v-else-if="editMode && profileLoaded" class="profile-edit">
            <div class="card">
                <h3 class="text-primary">Edit Profile Information</h3>
                
                <form @submit.prevent="updateProfile">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input v-model="full_name" type="text" placeholder="Full Name" required />
                    </div>
            
                    <div class="form-group">
                        <label>Branch</label>
                        <input v-model="branch" type="text" placeholder="Branch" required />
                    </div>
            
                    <div class="form-group">
                        <label>CGPA</label>
                        <input v-model="cgpa" type="number" step="0.01" placeholder="CGPA" required />
                    </div>
            
                    <div class="form-group">
                        <label>Graduation Year</label>
                        <input v-model="graduation_year" type="number" placeholder="Graduation Year" required />
                    </div>
            
                    <div class="form-group">
                        <label>Skills</label>
                        <input v-model="skills" type="text" placeholder="Skills (comma separated)" required />
                    </div>
            
                    <div class="form-group">
                        <label>Resume Link</label>
                        <input v-model="resume" type="url" placeholder="Resume Link" required />
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-primary">💾 Save Changes</button>
                        <button type="button" @click="toggleEditMode" class="btn-secondary">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- No Profile - Create Form -->
        <div v-else class="profile-create">
            <div class="card">
                <h3 class="text-primary">📝 Create Your Student Profile</h3>
                <p class="text-secondary">Fill in your information to create your student profile. This will help companies learn more about you.</p>
        
                <form @submit.prevent="createProfile">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input v-model="full_name" type="text" placeholder="Enter your full name" required />
                    </div>
            
                    <div class="form-group">
                        <label>Branch</label>
                        <input v-model="branch" type="text" placeholder="e.g., Computer Science" required />
                    </div>
            
                    <div class="form-group">
                        <label>CGPA</label>
                        <input v-model="cgpa" type="number" step="0.01" placeholder="e.g., 8.5" required />
                    </div>
            
                    <div class="form-group">
                        <label>Graduation Year</label>
                        <input v-model="graduation_year" type="number" placeholder="e.g., 2026" required />
                    </div>
            
                    <div class="form-group">
                        <label>Skills</label>
                        <input v-model="skills" type="text" placeholder="e.g., Java, Python, React, Node.js" required />
                    </div>
            
                    <div class="form-group">
                        <label>Resume Link</label>
                        <input v-model="resume" type="url" placeholder="https://example.com/resume.pdf" required />
                    </div>

                    <button type="submit" class="btn-primary" style="width: 100%;">✨ Create Profile</button>
                </form>
            </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error mt-3">{{ errorMessage }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const profile = ref({})
const profileLoaded = ref(false)
const profileExists = ref(false)
const editMode = ref(false)
const loading = ref(true)
const errorMessage = ref("")

const full_name = ref("")
const branch = ref("")
const cgpa = ref("")
const graduation_year = ref("")
const skills = ref("")
const resume = ref("")

const loadProfile = async () => {
    loading.value = true
    errorMessage.value = ""
    
    try {
        const token = localStorage.getItem("token")

        const res = await axios.get(
            "http://127.0.0.1:5000/fulluserprofile", {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        profile.value = res.data
        profileLoaded.value = true
        profileExists.value = true
        editMode.value = false
        loading.value = false
    } catch (error) {
        // Profile doesn't exist
        profileLoaded.value = true
        profileExists.value = false
        editMode.value = false
        loading.value = false
        errorMessage.value = ""
    }
}

const createProfile = async () => {
    try {
        errorMessage.value = ""
        const token = localStorage.getItem("token")

        await axios.post(
            "http://127.0.0.1:5000/fulluserprofile", {
                full_name: full_name.value,
                branch: branch.value,
                cgpa: cgpa.value,
                graduation_year: graduation_year.value,
                skills: skills.value,
                resume: resume.value
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        // Clear form
        full_name.value = ""
        branch.value = ""
        cgpa.value = ""
        graduation_year.value = ""
        skills.value = ""
        resume.value = ""

        // Reload profile to show it
        await loadProfile()
        alert("✅ Profile created successfully!")
    } catch (error) {
        errorMessage.value = error.response?.data?.error || "Failed to create profile"
        console.error("Create profile error:", error)
    }
}

const updateProfile = async () => {
    try {
        errorMessage.value = ""
        const token = localStorage.getItem("token")

        await axios.put(
            "http://127.0.0.1:5000/fulluserprofile", {
                full_name: full_name.value,
                branch: branch.value,
                cgpa: cgpa.value,
                graduation_year: graduation_year.value,
                skills: skills.value,
                resume: resume.value
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        // Reload profile to show updated info
        await loadProfile()
        alert("✅ Profile updated successfully!")
    } catch (error) {
        errorMessage.value = error.response?.data?.error || "Failed to update profile"
        console.error("Update profile error:", error)
    }
}

const toggleEditMode = () => {
    if (!editMode.value && profileExists.value) {
        // Populate form with current profile data
        full_name.value = profile.value.full_name
        branch.value = profile.value.branch
        cgpa.value = profile.value.cgpa
        graduation_year.value = profile.value.graduation_year
        skills.value = profile.value.skills
        resume.value = profile.value.resume
    } else {
        // Clear form
        full_name.value = ""
        branch.value = ""
        cgpa.value = ""
        graduation_year.value = ""
        skills.value = ""
        resume.value = ""
    }
    editMode.value = !editMode.value
}

onMounted(() => {
    loadProfile()
})
</script>